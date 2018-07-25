'''处理图片警告模块


'''
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class filedialogdemo(QWidget):
    def __init__(self, parent=None):
        super(filedialogdemo, self).__init__(parent)
        layout = QVBoxLayout()
        self.btn = QPushButton("加载图片")
        self.btn.clicked.connect(self.getfile)
        layout.addWidget(self.btn)
        self.le = QLabel("")
        layout.addWidget(self.le)
        self.setLayout(layout)
        self.setWindowTitle("File Dialog 例子")

    def getfile(self):
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Open file', '~', "Image files (*.jpg *.gif *.png * bmp)")
        self.le.setPixmap(QPixmap(fname))
        # 处理图片警告
        print(fname)
        img = QImage()
        img.load(fname)
        img.save(fname)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = filedialogdemo()
    ex.show()
    sys.exit(app.exec_())
