# Plotting tools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import threading
from chaosmap import Key_generator

#Image container and key generators
from img_data import img_data
import chaosmap
from math import e

def scatter_plot(r,g,b):
    fig = plt.figure()
    plot = fig.add_subplot(1, 1, 1, projection="3d")  # 3D plot with scalar values in each axis
    plot.scatter(r, g, b, c="r")
    plot.set_xlabel("Red")
    plot.set_ylabel("Green")
    plot.set_zlabel("Blue")
    plt.show()

def np_rgb_separation(img,r,g,b):
    for row in img:
        for pixel in row:
            r.append(pixel[0])
            g.append(pixel[1])
            b.append(pixel[2])

def encryption(image, seed_enc):
    lock_key = Key_generator(row_size_in=512, column_size_in=512, seed_in=seed_enc)
    lock_key.logistic_map_generation()
    image.fft()
    image.phase_mask(lock_key.key_map)
    #image.recover()
    image.copy()

def decryption(image, seed_dec):
    unlock_key = Key_generator(row_size_in=512, column_size_in=512, seed_in=seed_dec)
    unlock_key.logistic_map_generation()
    image.phase_unmask(unlock_key.key_map)
    image.recover()
    image.copy()

#Top module
def main():
    img_file = np.array(Image.open('lena.ppm'))
    r = []
    g = []
    b = []

    image = img_data(512,512)
    image.capture(img_file)
    image.RGB_sort()

    encryption(image,0.88)
    decryption(image,0.88)
    plt.imshow(image.img)
    plt.show()


if __name__ =='__main__':
    main()

