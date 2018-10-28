import numpy as np
import numpy
import gc
from chaosmap import KeyGenerator
import copy


class RGB_Image:
    R = []
    G = []
    B = []
    R_real = []
    R_imag = []
    G_real = []
    G_imag = []
    B_real = []
    B_imag = []
    R_SAVE = None
    G_SAVE = None
    B_SAVE = None


class ImgProcessor:

    def clean(self):
        self.RGBimage.R = []
        self.RGBimage.G = []
        self.RGBimage.B = []
        self.img_real = []
        self.img_imag = []
        gc.collect()

    def __init__(self, row, column):
        self.row_size = row
        self.column_size = column
        self.RGBimage = RGB_Image()
        self.img_real = []
        self.img_imag = []

    def capture(self, image):
        self.img_real = image
        self.img_imag = []
        self.RGB_sort()

    def RGB_sort(self):
        count = -1
        for row in self.img_real:
            count = count+1
            self.RGBimage.R.append([])
            self.RGBimage.G.append([])
            self.RGBimage.B.append([])

            for pixel in row:
                self.RGBimage.R[count].append(pixel[0])
                self.RGBimage.G[count].append(pixel[1])
                self.RGBimage.B[count].append(pixel[2])

    def copy(self):
        self.img_real = []
        self.img_imag = []

        for row in range(0, self.row_size):
            self.img_real.append([])
            for column in range (0, self.column_size):
                self.img_real[row].append([numpy.uint8(self.RGBimage.R_real[row][column]), numpy.uint8(self.RGBimage.G_real[row][column]), numpy.uint8(self.RGBimage.B_real[row][column])])
                self.img_real[row].append([numpy.uint8(self.RGBimage.R_real[row][column] >> 8), numpy.uint8(self.RGBimage.G_real[row][column] >> 8), numpy.uint8(self.RGBimage.B_real[row][column] >> 8)])
        self.img_real = np.array(self.img_real)

        for row in range(0, self.row_size):
            self.img_imag.append([])
            for column in range (0, self.column_size):
                self.img_imag[row].append([numpy.uint8(self.RGBimage.R_imag[row][column]),
                                           numpy.uint8(self.RGBimage.G_imag[row][column]),
                                           numpy.uint8(self.RGBimage.B_imag[row][column])])
                self.img_imag[row].append([numpy.uint8(self.RGBimage.R_imag[row][column] >> 8),
                                           numpy.uint8(self.RGBimage.G_imag[row][column] >> 8),
                                           numpy.uint8(self.RGBimage.B_imag[row][column] >> 8)])
        self.img_imag = np.array(self.img_imag)

        self.RGBimage.R_SAVE = copy.copy(self.RGBimage.R)


    def fft(self):
        self.R_freq = np.fft.fft2(self.RGBimage.R)
        self.G_freq = np.fft.fft2(self.RGBimage.G)
        self.B_freq = np.fft.fft2(self.RGBimage.B)

    def recover(self):
        self.RGBimage.R = np.fft.ifft2(self.R_freq)
        self.RGBimage.G = np.fft.ifft2(self.G_freq)
        self.RGBimage.B = np.fft.ifft2(self.B_freq)
        self.RGBimage.R_real = np.uint16(np.real(self.RGBimage.R))
        self.RGBimage.G_real = np.uint16(np.real(self.RGBimage.G))
        self.RGBimage.B_real = np.uint16(np.real(self.RGBimage.B))
        self.RGBimage.R_imag = np.uint16(np.imag(self.RGBimage.R))
        self.RGBimage.G_imag = np.uint16(np.imag(self.RGBimage.G))
        self.RGBimage.B_imag = np.uint16(np.imag(self.RGBimage.B))

    def wrap(self):
        self.img_real = []
        self.img_imag = []

        for row in range(0, self.row_size):
            self.img_real.append([])
            for column in range (0, self.column_size):
                self.img_real[row].append(
                    [numpy.uint8(self.RGBimage.R_real[row][column]), numpy.uint8(self.RGBimage.G_real[row][column]),
                     numpy.uint8(self.RGBimage.B_real[row][column])])
        self.img_real = np.array(self.img_real)

        for row in range(0, self.row_size):
            self.img_imag.append([])
            for column in range (0, self.column_size):
                self.img_imag[row].append([numpy.uint8(self.RGBimage.R_imag[row][column]),
                                           numpy.uint8(self.RGBimage.G_imag[row][column]),
                                           numpy.uint8(self.RGBimage.B_imag[row][column])])
        self.img_imag = np.array(self.img_imag)

    def phase_mask(self, key):
        for x in range (0, self.row_size):
            for y in range (0, self.column_size):
                self.R_freq[x][y] *= key[x][y]
                self.G_freq[x][y] *= key[x][y]
                self.B_freq[x][y] *= key[x][y]

    def phase_unmask(self, key):
        for x in range(0, self.row_size):
            for y in range(0, self.column_size):
                self.R_freq[x][y] /= key[x][y]
                self.G_freq[x][y] /= key[x][y]
                self.B_freq[x][y] /= key[x][y]

    def encryption(self, image, seed_enc):
        self.capture(image)
        lock_key = KeyGenerator(row_size_in=512, column_size_in=512, seed_in=seed_enc)
        lock_key.logistic_map_generation()
        self.fft()
        self.phase_mask(lock_key.key_map)
        self.recover()
        self.copy()

    def sign_conversion(self, arg):
        if np.uint16(arg) > 2 ** 15:
            return np.int32(np.uint32(arg) - 2 ** 16)
        else:
            return np.int32(arg)

    def decryption(self, key_img1, key_img2, seed_dec):
        self.key_img1 = key_img1
        self.key_img2 = key_img2

        for row in range(0, self.row_size):
            for column in range (0, int(self.column_size*2)):
                self.key_img1[row][column][0] = np.int32(self.key_img1[row][column][0])
                self.key_img1[row][column][1] = np.int32(self.key_img1[row][column][1])
                self.key_img1[row][column][2] = np.int32(self.key_img1[row][column][2])
                self.key_img2[row][column][0] = np.int32(self.key_img2[row][column][0])
                self.key_img2[row][column][1] = np.int32(self.key_img2[row][column][1])
                self.key_img2[row][column][2] = np.int32(self.key_img2[row][column][2])
        self.clean()

        for row in range(0, self.row_size):
            self.RGBimage.R.append([])
            self.RGBimage.G.append([])
            self.RGBimage.B.append([])
            for column in range(0, self.column_size):
                self.RGBimage.R[row].append(
                                                numpy.uint16(self.key_img1[row][2*column][0] + self.key_img1[row][2*column+1][0] * 128) +
                                                1j * numpy.uint16(self.key_img2[row][2*column][0] + self.key_img2[row][2*column+1][0] * 128 )
                                            )
                self.RGBimage.G[row].append(
                                            numpy.uint16(self.key_img1[row][2*column][1] + self.key_img1[row][2*column+1][1] * 128) +
                                            1j * numpy.uint16(self.key_img2[row][2*column][1] + self.key_img2[row][2*column+1][1] * 128)
                                            )
                self.RGBimage.B[row].append(
                                            self.key_img1[row][2*column][2] + self.key_img1[row][2*column+1][2] * 128 +
                                            1j * self.sign_conversion(self.key_img2[row][2*column][2] + self.key_img2[row][2*column+1][2] * 128)
                                            )
                print(str(self.RGBimage.R_SAVE[row][column]) + " " + str(self.RGBimage.R[row][column]))

        unlock_key = KeyGenerator(row_size_in=512, column_size_in=512, seed_in=seed_dec)
        unlock_key.logistic_map_generation()
        self.fft()
        self.phase_unmask(unlock_key.key_map)
        self.recover()
        self.wrap()

    def showPixelData(self):
        print("R Data\n" + self.R)
        print("G Data \n" + self.G)
        print("B Data \n" + self.B)
