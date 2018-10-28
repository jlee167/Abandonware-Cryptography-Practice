# Plotting tools
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import threading

#Image container and key generators
from imgdata import ImgProcessor


class BackendController:

    def __init__(self):
        self.ImgHandler = ImgProcessor(512, 512)
        pass

    def bg_prompt(self):
        while (True):
            Operation = input("Command (DEC for decryption, ENC for encryption):")

            if Operation == "ENC":
                filename = "image" + "/" + input("Image file name:")
                self.KEY = input("KEY (floating point between 0.0 and 1.0):")
                print("Image " + filename + " registered.")

                self.ImgHandler.encryption(np.array(Image.open(filename)), float(self.KEY))
                a = Image.fromarray(self.ImgHandler.img_real)
                a.save("out.ppm")
                a = Image.fromarray(self.ImgHandler.img_imag)
                a.save("out2.ppm")


            elif Operation == "DEC":
                filename_r = input("Encrypted file path:")
                filename_i = input("Encrypted file path2:")
                self.img_real = np.array(Image.open(filename_r))
                """
                for row in range (0, 511):
                    for column in range (0,511):
                        print(str(self.ImgHandler.img_real[row][column]) + " " + str(new[row][column]))
                """
                self.img_imag = np.array(Image.open(filename_i))
                self.KEY = input("KEY (floating point between 0.0 and 1.0):")

                self.ImgHandler.decryption(self.img_real, self.img_imag, float(self.KEY))

                plt.imshow(self.ImgHandler.img_real)
                plt.show()
                plt.imshow(self.ImgHandler.img_imag)
                plt.show()


            elif Operation == "QUIT":
                break

            else:
                pass


if __name__ == '__main__':
    new_instance = BackendController()
    new_instance.bg_prompt()

