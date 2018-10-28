import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PIL import ImageQt, Image

app = QApplication(sys.argv)

class GUI (QWidget):
    def __init__(self):
        super().__init__()
        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('FFT Cryptographer')

        self.label = QLabel(self)
        self.image = Image.open('image/lena.ppm')
        self.image = self.image.resize((256, 256))
        self.image.show()

        self.image = ImageQt.ImageQt(self.image)
        self.pixmap = QPixmap.fromImage(self.image)
        self.label.setPixmap(self.pixmap)

        self.resize(1024, 1024)
        self.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    GUI_obj = GUI()