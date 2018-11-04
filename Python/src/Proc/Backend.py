# Plotting tools
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import threading

#Image container and key generators
from Crypt_FFT import ImgProcessor
from Crypt_AES import AESCryptor
from frontend_QtGUI import QtGUI
import os
import gc


class BackendObject:

    def __init__(self):
        pass

    def OP_FFT_ENC(self, filename, key):
        ImgHandler = ImgProcessor(512, 512)
        ImgHandler.encryption(np.array(Image.open(filename)), float(key))
        a = Image.fromarray(ImgHandler.img_real)
        a.save("out.ppm")
        a = Image.fromarray(ImgHandler.img_imag)
        a.save("out2.ppm")

    def OP_FFT_DEC(self, filename_r, filename_i, key):
        ImgHandler = ImgProcessor(512, 512)
        img_real = np.array(Image.open(filename_r))
        img_imag = np.array(Image.open(filename_i))
        KEY = input("KEY (floating point between 0.0 and 1.0):")
        ImgHandler.decryption(img_real, img_imag, float(key))
        out_img = Image.fromarray(ImgHandler.img_real)
        out_img.save("decrypted.ppm")

    def OP_AES_ENC(self, filename, key, outfile):
        image_orig = np.array(Image.open(filename))
        row_size = image_orig.shape[0]
        column_size = image_orig.shape[1]
        AEShandler = AESCryptor(row_size, column_size, image_orig, key)
        AEShandler.encrypt()
        AESImage = Image.fromarray(AEShandler.return_new_image())
        AESImage.save(outfile)

    def OP_AES_DEC(self, filename, key, outfile):
        image_orig = np.array(Image.open(filename))
        row_size = image_orig.shape[0]
        column_size = image_orig.shape[1]
        AEShandler = AESCryptor(row_size, column_size, image_orig, key)
        AEShandler.decrypt()
        AESImage = Image.fromarray(AEShandler.return_new_image())
        AESImage.save(outfile)

if __name__ == '__main__':
    try:
        BackendController = BackendObject()
    except Exception:
        print(Exception)
    GUI = QtGUI(BackendController)