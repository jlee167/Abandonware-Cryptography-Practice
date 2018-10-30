# Plotting tools
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import threading

#Image container and key generators
from imgdata import ImgProcessor
from Crypto.Cipher import AES
from Crypto import Random
import os
import queue
import binascii


class BackendController:

    def __init__(self):
        self.ImgHandler = ImgProcessor(512, 512)
        pass

    def bg_prompt(self):
        while (True):
            Operation = input("Command (DEC for decryption, ENC for encryption):")

            if Operation == "FFT_ENC":
                filename = "image" + "/" + input("Image file name:")
                self.KEY = input("KEY (floating point between 0.0 and 1.0):")
                print("Image " + filename + " registered.")

                self.ImgHandler.encryption(np.array(Image.open(filename)), float(self.KEY))
                a = Image.fromarray(self.ImgHandler.img_real)
                a.save("out.ppm")
                a = Image.fromarray(self.ImgHandler.img_imag)
                a.save("out2.ppm")


            elif Operation == "FFT_DEC":
                filename_r = input("Encrypted file path:")
                filename_i = input("Encrypted file path2:")
                self.img_real = np.array(Image.open(filename_r))
                self.img_imag = np.array(Image.open(filename_i))
                self.KEY = input("KEY (floating point between 0.0 and 1.0):")

                self.ImgHandler.decryption(self.img_real, self.img_imag, float(self.KEY))
                out_img = Image.fromarray(self.ImgHandler.img_real)
                out_img.save("decrypted.ppm")
                plt.imshow(self.ImgHandler.img_real)
                plt.show()
                plt.imshow(self.ImgHandler.img_imag)
                plt.show()

            elif Operation == "AES_ENC":
                filename_aes = "image" + "/" + input("Image file name:")
                print("Image " + filename_aes + " registered.")
                self.image_orig = np.array(Image.open(filename_aes))

                # Initializing Vector
                IV = Random.new().read(16)
                key = Random.new().read(16)
                self.new_img = np.array(np.zeros(shape=(512, 512, 3)))

                #IV = binascii.unhexlify(IV)
                #key = binascii.unhexlify(key)
                self.aes_rgbchannel(IV, key, 0)
                self.aes_rgbchannel(IV, key, 1)
                self.aes_rgbchannel(IV, key, 2)

                self.new_img = self.new_img.astype(dtype=np.uint8)
                print(type(self.new_img[0][0][0]))
                AESImage = Image.fromarray(self.new_img)
                AESImage.save("AES_LENA.ppm")

            elif Operation == "AES_DEC":
                pass

            elif Operation == "QUIT":
                break

            else:
                pass

    def aes_rgbchannel(self, IV, key, rgb_index):
        plaintext = []
        encrypted_text_FIFO = queue.Queue()
        encryptor = AES.new(key, AES.MODE_CBC, IV=IV)

        for row in range(0, 512):
            for column in range(0, 512):
                plaintext.append(self.image_orig[row][column][rgb_index])
                if len(plaintext) < 16:
                    pass
                else:
                    result = encryptor.encrypt(plaintext=bytes(plaintext))
                    result = bytes(result)
                    for bytedata in result:
                        encrypted_text_FIFO.put(np.uint8(bytedata))
                    plaintext = []

        for row in range(0, 512):
            for column in range(0, 512):
                self.new_img[row][column][rgb_index] = np.uint8(encrypted_text_FIFO.get())


if __name__ == '__main__':
    new_instance = BackendController()
    new_instance.bg_prompt()

