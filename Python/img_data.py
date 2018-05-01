import numpy as np

class img_data:
    R = []
    G = []
    B = []
    def __init__(self, row, column):
        self.row_size = row
        self.column_size = column
        return

    def capture(self,image):
        self.img = image

    def RGB_sort(self):
        count = -1
        for row in self.img:
            count = count+1
            self.R.append([])
            self.G.append([])
            self.B.append([])

            for pixel in row:
                self.R[count].append(pixel[0])
                self.G[count].append(pixel[1])
                self.B[count].append(pixel[2])

    def fft(self):
        self.R = np.fft.fft2(self.R)
        self.G = np.fft.fft2(self.G)
        self.B = np.fft.fft2(self.B)

    def recover(self):
        self.R = np.real(np.fft.ifft2(self.R))
        self.G = np.real(np.fft.ifft2(self.G))
        self.B = np.real(np.fft.ifft2(self.B))


    def copy(self):
        row_counter = -1
        for row in self.img:
            row_counter = row_counter + 1
            counter = 0
            for pixel in row:
                pixel[0] = self.R[row_counter][counter]
                pixel[1] = self.G[row_counter][counter]
                pixel[2] = self.B[row_counter][counter]
                counter = counter + 1

    def phase_mask(self, key):
        for x in range (0, self.row_size):
            for y in range (0, self.column_size):
                self.R[x][y] *= key[x][y]
                self.G[x][y] *= key[x][y]
                self.B[x][y] *= key[x][y]
    def phase_unmask(self, key):
        for x in range (0, self.row_size):
            for y in range (0, self.column_size):
                self.R[x][y] /= key[x][y]
                self.G[x][y] /= key[x][y]
                self.B[x][y] /= key[x][y]

    def print(self):
        print(self.R)
        print(self.G)
        print(self.B)
