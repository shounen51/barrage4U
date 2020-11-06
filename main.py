'''
⠄⠄⠈⣿⠄⠄⠄⢙⢞⢿⣿⢹⢿⣦⢏⣱⢿⠘⣿⣝⠹⢿⣿⡽⣿⣿⣏⣆⢿⣿⡞⠁
⠄⠄⠄⢻⡀⠄⠄⠈⣾⡸⡏⢸⡾⣴⣿⣿⣶⣼⣎⢵⢀⡛⣿⣷⡙⡻⢻⡴⠨⠨⠖⠃
⠄⠄⠄⠈⣧⢀⡴⠊⢹⠁⡇⠈⢣⣿⣿⣿⣿⣦⣿⣷⣜⡳⣝⢧⢃⢣⣼⢁⠘⠆⠄⠄
⠄⠄⠄⠄⢹⡇⠄⣠⠔⠚⣅⠄⢰⣶⣦⣭⣿⣿⣿⡿⠟⠿⣷⡧⠄⣘⣟⣸⠄⠄⠄⠄
⠄⠄⠄⠄⠄⢷⠎⠄⠄⠄⣼⣦⠻⣿⣿⡟⠛⠻⢿⣿⣿⣿⡾⢱⣿⡏⠸⡏⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠸⡄⠄⡄⠄⣿⢧⢗⠌⠻⣇⠿⠿⣸⣿⣿⡟⡐⣿⠟⢰⣇⠇⠄⠄⠄⠄
⠄⠄⠄⠄⠄⣠⡆⠄⠃⢠⠏⣤⢀⢢⡰⣭⣛⡉⠩⠭⡅⣾⢳⡴⡀⢸⣿⡆⠄⠄⠄⠄
⠄⠄⠄⢀⣶⡟⣽⠼⢀⡕⢀⠘⠸⢮⡳⡻⡍⡷⡆⠤⠤⠭⢸⢳⣷⢸⡟⣷⠄⠄⠄⠄
'''
"""[summary]
    V1.1
    最新更新:
        儲存設定
    status:
        0: 未登入
        1: 登入中
        2: 彈幕啟動中
"""
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Barrage4U")
import os
import sys
import time
import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.sip
import discord

import icon
from ui.A import A_form
from ui.full_screen import B_form
from utils.button_event import btn_events
from utils.utils import load_ini, save_ini
from utils.bot_thread import bot_thread
from barrage_types.classic_type import Btype_CLASSIC_thread
from configs import bot_list, default_setting


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        myicon = QIcon()
        myicon.addPixmap(QPixmap("src/icon.ico"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(myicon)
        OK, self.setting = load_ini('./setting.ini')
        self.event = btn_events(self)
        self.ui = A_form(self, self.event)
        self.canvas = B_form(self.from_setting)
        long_limit = self.from_setting('barrage', 'long_limit', 'int')
        self.bot = bot_thread(self, long_limit=long_limit)
        self.barrage_thread = Btype_CLASSIC_thread(self.bot, self.canvas, self)
        self.barrage_thread.new_signal.connect(self.barrage_thread.ui_new_label)
        self.barrage_thread.move_signal.connect(self.barrage_thread.ui_move_label)
        self.status = 0
        self.set_status(self.status)
        self.platform = ""

    def login(self):
        self.ui.login()
        self.barrage_thread.start()
        self.set_status(2)

    def set_status(self, status):
        self.status = status
        # if status == 0:
        #     self.ui.label_main.setStyleSheet('QLabel {background-image : url("./src/waiting.png")}')
        #     self.ui.btn_login.setText('登入頻道')
        # elif status == 1:
        #     self.ui.label_main.setStyleSheet('QLabel {background-image : url("./src/logining.png")}')
        #     self.ui.btn_login.setText('登入中')
        # elif status == 2:
        #     self.ui.label_main.setStyleSheet('QLabel {background-image : url("./src/fire.png")}')
        #     self.ui.btn_login.setText('登入完成')

    def set_platform_when_logining(self, platform):
        self.platform = platform
        self.canvas.emotes.set_platform(self.platform)

    def what_platform_now(self):
        return self.platform

    def from_setting(self, major_key, detail_key, _type='str'):
        try:
            value = self.setting[major_key][detail_key]
        except:
            logging.info('Use setting fail. Use default setting')
            if major_key in self.setting:
                self.setting[major_key][detail_key] = default_setting[major_key][detail_key]
            else:
                self.setting[major_key] = default_setting[major_key]
            value = self.setting[major_key][detail_key]
        """type"""
        if _type == 'str' or _type == 'string':
            pass
        elif _type == 'bool' or _type == 'boolean':
            if value.startswith('T') or value.startswith('t'):
                value = True
            else:
                value = False
        elif _type == 'int':
            value = int(value)
        return value

    def modfy_setting(self, major_key, detail_key, value):
        self.setting[major_key][detail_key] = str(value)

    def closeEvent(self, event):
        self.bot.close()
        self.barrage_thread.stop()
        self.barrage_thread.wait()
        self.canvas.close()
        self.canvas.deleteLater()
        save_ini('./setting.ini', self.setting)
        logging.info('Close normally.')

if __name__ == "__main__":
    if not os.path.isdir('./log'):
        os.mkdir('./log')
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[logging.FileHandler('log/last.log', 'w', 'utf-8'), ])

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.canvas.show()
    # win.setFocus(Qt.MouseFocusReason)
    """auto connect"""
    auto_connect = win.from_setting('basic', 'auto_connect', 'bool')
    if auto_connect:
        win.ui.btn_login.click()
    sys.exit(app.exec_())