import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PIL import ImageQt, Image
import gc
import threading


app = QApplication(sys.argv)


class QtGUI (QMainWindow):

    def __init__(self, backend_object):
        super().__init__()
        self.BackendControl = backend_object
        self.parent = 0
        self.resize(2048, 2048)
        self.move(300, 300)
        self.setWindowTitle('FFT Cryptographer')

        self.label = QLabel(self)
        self.image = Image.open('image/lena.ppm')
        self.image = self.image.resize((256, 256))
        self.image = ImageQt.ImageQt(self.image)
        self.pixmap = QPixmap.fromImage(self.image)
        self.label.setPixmap(self.pixmap)
        self.label.resize(512, 512)
        self.label.move(0, 0)
        self.label_cipherimg = QLabel(self)

        self.initUI()
        self.show()
        sys.exit(app.exec_())

    def initUI(self):
        self.encrypt_btn = QPushButton("Encrypt", self)
        self.encrypt_btn.move(256, 256)
        self.encrypt_btn.clicked.connect(self.encrypt)

    def encrypt(self):
        self.encrypted_image = Image.open('lena.jpg')
        self.encrypted_image = self.encrypted_image.resize((128, 128))
        self.encrypted_image = ImageQt.ImageQt(self.encrypted_image)
        self.pixmap_cipherimg = QPixmap.fromImage(self.encrypted_image)
        self.label_cipherimg.resize(128, 128)
        self.label_cipherimg.setPixmap(self.pixmap_cipherimg)
        self.label.setPixmap(self.pixmap_cipherimg)
        self.label_cipherimg.move(300, 200)
        self.update()

    def onClick_loadImage(self, filename):
        self.image = Image.open(filename)
        self.image.resize(256,256)


    def onClick_AES_ENC(self, filename, ):
        self.encrypted_image =


if __name__ == '__main__':
    GUI_obj = QtGUI()