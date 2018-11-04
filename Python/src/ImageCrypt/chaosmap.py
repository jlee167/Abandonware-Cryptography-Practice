from math import cos
from math import sin
from math import pi


class KeyGenerator:

    """
    <KeyGen Parameters>
    1. SEED = Initial seed to the logistic map oscillation
    2. row_size, column_size: Pixel dimension of the image (i.e 512X512, 1024X1024)
    3. R = Bifurcation parameter
    4. key_map = storage for FFT Mask
    """
    def __init__ (self, row_size_in, column_size_in, seed_in):
        self.row_size = row_size_in         # Image size (pixel)
        self.column_size = column_size_in   # Image
        self.SEED = seed_in                 # Initial seed to logistics map
        self.R = 3.88                       # Multiplier must be between 3.75 and 4.00 to induce chaotic behavior
        self.key_map = []                   # (Row * Column) sized FFT phase mask

    def setSeed(self, DataIn):
        self.SEED = DataIn

    def getSeed(self, seed):
        return self.SEED

    def setBifurcationParam(self, dataIn):
        self.R = dataIn

    def getBifurcationParam(self):
        return self.R

    def setImageSize(self, Xdim, Ydim):
        self.row_size = Xdim
        self.column_size = Ydim

    def logisticComputation(self):
        self.SEED = (self.R * self.SEED) * (1 - self.SEED)

    def logistic_map_generation(self):
        for row in range (0, self.row_size):
            self.key_map_singlerow = []
            for column in range (0, self.column_size):
                self.key_map_singlerow.append(cos(self.SEED*2*pi) + (sin(self.SEED*2*pi) * 1j) )
                if int(column) == int(self.column_size - 1):
                    self.key_map.append(self.key_map_singlerow)
                self.logisticComputation()