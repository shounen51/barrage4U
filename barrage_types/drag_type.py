import threading
import time
import math
import logging

from utils.barrage_class import barrage
from PyQt5.QtCore import QThread, pyqtSignal
import win32api


class Btype_DRAG_thread(QThread):
    new_signal = pyqtSignal(dict)
    move_signal = pyqtSignal(dict)
    def __init__(self, bot, canvas, main):
        super().__init__()
        