__author__ = 'patrick'

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QCoreApplication

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def home(self):
        button = QPushButton('Exit', self)
        button.clicked.connect(QCoreApplication.instance().quit)

        self.show()



    def init_ui(self):
        self.resize(500, 300)
        self.center()
        self.setWindowTitle("Hello World")
        self.home()
        # print(self.setWindowIcon(QIcon('favicon.ico')), "yes")
        # print(self.setWindowIcon(QIcon('favicon.ico')))
        self.show()

    def center(self):
        qr = self.frameGeometry()

        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())


if __name__ == "__main__":
    import os
    app = QApplication(sys.argv)
    # path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'favicon.ico')
    # app.setWindowIcon(QIcon(path))
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)

    Window = Window()
    sys.exit(app.exec())

