# Plotting tools
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import threading

#Image container and key generators
from Python.src.ImageCrypt.Crypt_FFT import ImgProcessor
from Python.src.ImageCrypt.Crypt_AES import AESCryptor
import os
import gc


class backendobject:

    def __init__(self):
        pass

    def OP_FFT_ENC(self, image, key):
        ImgHandler = ImgProcessor(512, 512)
        ImgHandler.encryption(np.array(image), float(key))
        a = Image.fromarray(ImgHandler.img_real)
        a.save("out.ppm")
        a = Image.fromarray(ImgHandler.img_imag)
        a.save("out2.ppm")

    def OP_FFT_DEC(self, image_r, image_i, key):
        ImgHandler = ImgProcessor(512, 512)
        img_real = np.array(image_r)
        img_imag = np.array(image_i)
        KEY = input("KEY (floating point between 0.0 and 1.0):")
        ImgHandler.decryption(img_real, img_imag, float(key))
        out_img = Image.fromarray(ImgHandler.img_real)
        out_img.save("decrypted.ppm")

    def OP_AES_ENC(self, image, key, outfile):
        image_orig = np.array(image)
        row_size = image_orig.shape[0]
        column_size = image_orig.shape[1]
        AEShandler = AESCryptor(row_size, column_size, image_orig, key)
        AEShandler.encrypt()
        AESImage = Image.fromarray(AEShandler.return_new_image())
        AESImage.save(outfile)

    def OP_AES_DEC(self, image, key, outfile):
        image_orig = np.array(image)
        row_size = image_orig.shape[0]
        column_size = image_orig.shape[1]
        AEShandler = AESCryptor(row_size, column_size, image_orig, key)
        AEShandler.decrypt()
        AESImage = Image.fromarray(AEShandler.return_new_image())
        AESImage.save(outfile)
