import serial
import scipy.misc
import matplotlib.pyplot as plt
import numpy
import time
from PIL import Image
import io


#img = scipy.misc.imread('lena.ppm')
#img = scipy.misc.imresize(img, (256, 256))
img = Image.open('lena_1_128x128.jpg')
img = numpy.array(img)

'''
for row in range (0,128):
    if row%4 == 0:
        filename = "%d" % (row/4)
        print(filename)
        file = open(filename,"wb")
    for column in range (0,128):
        for rgb in range (0,3):
            file.write(img[row][column][rgb])

print(img)
'''

f = open("output.bin", "rb")
a = numpy.fromfile(f, dtype=numpy.uint8)
print(a)
f.close()


k = 0
for row in range (0,128):
    for column in range (0,128):
        for rgb in range (0,3):
             try:
                img[row][column][rgb] = a[k]
                k = k + 1
                print(k)
             except:
                print("Data not present")
                k = k + 1
print(img[10])
plt.imshow(img)
plt.show()




'''
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM5'
ser.open()

for row in range (0,128):
    for column in range (0, 128):
        for color in range(0, 3):
            ser.write(img[row][column][color].tobytes())
            print(row, column, color)
'''


'''
while ser.in_waiting() is 0:
    plt.show()

for color in range (0,2):
    for row in range (0,511):
        for column in range (0, 511):
            img[row][column][color] = ser.read(1)

plt.imshow(img)
plt.show()


ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM5'
ser.open()
print(ser.write(b'hello'))
plt.imshow(img)
plt.show()
'''