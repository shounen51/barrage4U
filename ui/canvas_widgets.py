from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.sip

class canvas_win(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        #self.setStyleSheet('QWidget {background-color: #FFFFFF; color: #000000;}')

class canvas_label(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.BypassWindowManagerHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setStyleSheet('QLabel {background-color: #FFFFFF; color: #000000;}')

class canvas_label_back(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.setStyleSheet('QLabel {background-color: #FFFFFE; color: #FFFFFE;}')