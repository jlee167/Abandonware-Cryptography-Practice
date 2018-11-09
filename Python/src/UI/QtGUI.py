import sys
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMainWindow, QGroupBox, QFormLayout, QLineEdit, \
                            QHBoxLayout, QVBoxLayout, QFileDialog
from PySide2.QtGui import QIcon, QPixmap, QImage
from PIL import ImageQt, Image
import threading

from Python.src.Proc.Backend import backendobject

app = QApplication(sys.argv)

class QtGUI (QMainWindow):

    def __init__(self):
        super().__init__()
        self.BackendControl = backendobject()
        self.parent = 0
        self.resize(2048, 2048)
        self.move(300, 300)
        self.setWindowTitle('FFT Cryptographer')

        """
        self.label = QLabel()
        self.image = Image.open('../../image/lena.ppm')
        self.image = self.image.resize((256, 256))
        #self.image = ImageQt.ImageQt(self.image)
        self.image = QImage('../../image/lena.ppm').scaled(256, 256)
        self.pixmap = QPixmap(self.image)
        self.label.setPixmap(self.pixmap)
        self.label.resize(256, 256)
        self.label.move(0, 0)
        """

        self.initUI()
        self.show()
        sys.exit(app.exec_())

    def initUI(self):
        self.statBar = self.statusBar()
        self.statBar.showMessage("Ready")

        self.origImageGroup = QGroupBox("Original Image")
        self.origImageGroup.move(200, 200)
        self.origImageGroup.resize(600, 200)

        self.origFilePath = QLineEdit()
        self.layout = QFormLayout()
        self.btn_filesearch = QPushButton("Search")
        self.btn_filesearch.resize(50, 50)
        self.btn_filesearch.clicked.connect(self.onClick_loadImage)
        self.layout.addRow(self.origFilePath, self.btn_filesearch)

        self.encrypt_key = QLineEdit()
        self.encrypt_btn = QPushButton("Encrypt", self)
        self.encrypt_btn.clicked.connect(self.onClick_AES_ENC)
        self.layout.addRow(self.encrypt_key)

        self.decrypt_btn = QPushButton("Decrypt", self)
        self.decrypt_btn.clicked.connect(self.onClick_AES_DEC)
        self.layout.addRow(self.decrypt_btn, self.encrypt_btn)

        self.img_orig = QLabel()
        self.img_cipher = QLabel()
        self.layout.addRow(self.img_orig, self.img_cipher)
        """
        self.image = Image.open('../../image/lena.ppm')
        self.image = self.image.resize((256, 256))
        #self.image = ImageQt.ImageQt(self.image)
        self.image = QImage('../../image/lena.ppm').scaled(256, 256)
        self.pixmap = QPixmap(self.image)
        self.label.setPixmap(self.pixmap)
        self.label.resize(256, 256)
        self.label.move(0, 0)
        """
        #self.layout.addRow(self.label)

        self.origImageGroup.setLayout(self.layout)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.origImageGroup)
        self.layoutcontiner = QWidget(self)
        self.layoutcontiner.resize(600, 500)
        self.layoutcontiner.setLayout(self.mainLayout)

    def onClick_loadImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/', "Image files (*.jpg *.gif)")
        print(fname[0])
        self.image = Image.open(str(fname[0]))
        showimage = QImage(str(fname[0])).scaled(256,256)
        newpixmap = QPixmap(showimage)
        self.img_orig.setPixmap(newpixmap)
        self.update()

    def onClick_AES_ENC(self):
        key = self.encrypt_key.text()
        self.BackendControl.OP_AES_ENC(self.image, key, "out.ppm")
        ciperpixmap = QPixmap(QImage("out.ppm").scaled(256, 256))
        self.img_cipher.setPixmap(ciperpixmap)
        self.update()

    def onClick_AES_DEC(self):
        key = self.encrypt_key.text()
        self.BackendControl.OP_AES_DEC(Image.open("out.ppm"), key, "out.ppm")
        ciperpixmap = QPixmap(QImage("out.ppm").scaled(256, 256))
        self.img_cipher.setPixmap(ciperpixmap)
        self.update()

if __name__ == '__main__':
    GUI_obj = QtGUI()