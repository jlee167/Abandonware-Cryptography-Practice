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
        self.resize(2048, 1024)
        self.move(300, 300)
        self.setWindowTitle('FFT Cryptographer')
        self.initUI()
        self.show()
        sys.exit(app.exec_())

    def initUI(self):
        self.statBar = self.statusBar()
        self.statBar.showMessage("Ready")

        self.origFilePath = QLineEdit()
        self.label_filename = QLabel()
        self.label_filename.setText("AES Source:")
        self.label_filename.resize(200, 50)
        self.btn_filesearch = QPushButton("Search")
        self.btn_filesearch.clicked.connect(self.onClick_loadImage)
        self.file_io_box = QHBoxLayout()
        self.file_io_box.addWidget(self.label_filename)
        self.file_io_box.addWidget(self.origFilePath)
        self.file_io_box.addWidget(self.btn_filesearch)

        #AES Control and File I/O Widgets
        self.label_AESKey = QLabel()
        self.label_AESKey.setText("AES Key:")
        self.label_AESKey.resize(200, 50)
        self.AESencrypt_key = QLineEdit()
        self.AESencrypt_btn = QPushButton("AES Encrypt", self)
        self.AESencrypt_btn.clicked.connect(self.onClick_AES_ENC)
        self.AESdecrypt_btn = QPushButton("AES Decrypt", self)
        self.AESdecrypt_btn.clicked.connect(self.onClick_AES_DEC)
        self.AES_layout = QHBoxLayout()
        self.AES_layout.addWidget(self.label_AESKey)
        self.AES_layout.addWidget(self.AESencrypt_key)
        self.AES_layout.addWidget(self.AESdecrypt_btn)
        self.AES_layout.addWidget(self.AESencrypt_btn)

        #FFT Control and File I/O Widgets
        self.FFTencrypt_btn = QPushButton("FFT Encrypt", self)
        self.FFTencrypt_btn.clicked.connect(self.onClick_FFT_ENC)
        self.FFTdecrypt_btn = QPushButton("FFT Decrypt", self)
        self.FFTdecrypt_btn.clicked.connect(self.onClick_FFT_DEC)

        self.img_orig = QLabel()
        self.img_cipher = QLabel()
        self.image_layout = QHBoxLayout()
        self.image_layout.addWidget(self.img_orig)
        self.image_layout.addWidget(self.img_cipher)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.file_io_box)
        self.mainLayout.addLayout(self.AES_layout)
        self.mainLayout.addLayout(self.image_layout)
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
        key = self.AESencrypt_key.text()
        self.BackendControl.OP_AES_ENC(self.image, key, "out.ppm")
        ciperpixmap = QPixmap(QImage("out.ppm").scaled(256, 256))
        self.img_cipher.setPixmap(ciperpixmap)
        self.update()

    def onClick_AES_DEC(self):
        key = self.AESencrypt_key.text()
        self.BackendControl.OP_AES_DEC(Image.open("out.ppm"), key, "out.ppm")
        ciperpixmap = QPixmap(QImage("out.ppm").scaled(256, 256))
        self.img_cipher.setPixmap(ciperpixmap)
        self.update()

    def onClick_FFT_ENC(self):
        pass

    def onClick_FFT_DEC(self):
        pass

if __name__ == '__main__':
    GUI_obj = QtGUI()