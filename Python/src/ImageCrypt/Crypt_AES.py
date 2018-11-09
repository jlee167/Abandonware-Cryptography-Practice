from Crypto.Cipher import AES
from Crypto import Random
import numpy
import queue


class AESCryptor:

    def __init__(self, size_row, size_column, image_orig, key):
        # Set image size
        self.size_row = size_row
        self.size_column = size_column
        if (self.size_row % 16 != 0):
            self.size_fitrow = size_row + (16 - size_row % 16)
        else:
            self.size_fitrow = self.size_row

        if (self.size_column % 16 != 0):
            self.size_fitcolumn = size_column + (16 - size_column % 16)
        else:
            self.size_fitcolumn = self.size_column
        self.image_orig = image_orig
        self.key = key

        # Initializing Vector
        self.new_img = numpy.array(numpy.zeros(shape=(self.size_fitrow, self.size_fitcolumn, 3))).astype(numpy.uint8)

    def return_new_image(self):
        return self.new_img

    def encrypt(self):
        IV = Random.new().read(16)
        self.enc_singleRGBchannel(IV, self.key, 0)
        self.enc_singleRGBchannel(IV, self.key, 1)
        self.enc_singleRGBchannel(IV, self.key, 2)

    def enc_singleRGBchannel(self, IV, key, rgb_index):
        plaintext = []
        encrypted_text_FIFO = queue.Queue()
        encryptor = AES.new(key)#, AES.MODE_CBC, IV=IV)
        cnt = 0
        for row in range(0, self.size_fitrow):
            for column in range(0, self.size_fitcolumn):
                if ((row < self.size_row) and (column < self.size_column)):
                    plaintext.append(self.image_orig[row][column][rgb_index])
                else:
                    plaintext.append(numpy.uint8(0))
                cnt = cnt + 1
                if len(plaintext) < 16:
                    pass
                else:
                    result = encryptor.encrypt(plaintext=bytes(plaintext))
                    result = bytes(result)
                    for bytedata in result:
                        encrypted_text_FIFO.put(numpy.uint8(bytedata))
                    plaintext = []

        for row in range(0, self.size_fitrow):
            for column in range(0, self.size_fitcolumn):
                self.new_img[row][column][rgb_index] = numpy.uint8(encrypted_text_FIFO.get())

    def decrypt(self):
        IV = Random.new().read(16)
        self.dec_singleRGBchannel(IV, self.key, 0)
        self.dec_singleRGBchannel(IV, self.key, 1)
        self.dec_singleRGBchannel(IV, self.key, 2)

    def dec_singleRGBchannel(self, IV, key, rgb_index):
        ciphertext = []
        encrypted_text_FIFO = queue.Queue()
        encryptor = AES.new(key)  # , AES.MODE_CBC, IV=IV)

        for row in range(0, self.size_fitrow):
            for column in range(0, self.size_fitcolumn):
                ciphertext.append(self.image_orig[row][column][rgb_index])
                print(row)
                if len(ciphertext) < 16:
                    pass
                else:
                    result = encryptor.decrypt(ciphertext=bytes(ciphertext))
                    result = bytes(result)
                    for bytedata in result:
                        encrypted_text_FIFO.put(numpy.uint8(bytedata))
                    ciphertext = []

        for row in range(0, self.size_fitrow):
            for column in range(0, self.size_fitcolumn):
                self.new_img[row][column][rgb_index] = numpy.uint8(encrypted_text_FIFO.get())