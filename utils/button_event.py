import json
import time
import sys
from datetime import datetime
import random
import os
import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.sip

from configs import platform_list, default_setting
from utils.utils import save_ini

class btn_events():
    def __init__(self, main_window):
        self.main = main_window

    def edit_channel(self):
        logging.info('edit_channel edited')
        bot_platform = platform_list[self.main.ui.combo_platform.currentIndex()]
        bot_channel = self.main.ui.edit_channel.text()
        self.main.modfy_setting(bot_platform, 'channel', bot_channel)

    def btn_login(self):
        logging.info('btn_login clicked')
        self.main.set_status(1)
        bot_platform = platform_list[self.main.ui.combo_platform.currentIndex()]
        bot_channel = self.main.ui.edit_channel.text()
        OK = self.main.bot.login(bot_platform, bot_channel)
        if OK:
            self.main.modfy_setting('connect', 'platform', bot_platform)
            self.main.modfy_setting(bot_platform, 'channel', bot_channel)
        else:
            self.main.set_status(0)

    def btn_save(self):
        logging.info('btn_save clicked')
        try:
            bot_platform = platform_list[self.main.ui.combo_platform.currentIndex()]
            bot_channel = self.main.ui.edit_channel.text()

            Bontop = self.main.ui.cb_on_top.isChecked()
            Bcrosshair = self.main.ui.cb_avoid_crosshair.isChecked()
            Bscrolling = self.main.ui.edit_scrolling.text()

            Bname = self.main.ui.cb_show_name.isChecked()
            text = self.main.ui.edit_size.text()
            Bsize = abs(int(text))
            text = self.main.ui.edit_time.text()
            Btime = abs(int(text))
            Balpha = self.main.ui.sli_alpha.value()

            self.main.modfy_setting('connect', 'platform', bot_platform)
            self.main.modfy_setting(bot_platform, 'channel', bot_channel)
            self.main.modfy_setting('canvas', 'cover', Bontop)
            self.main.modfy_setting('canvas', 'avoid_crosshair', Bcrosshair)
            self.main.modfy_setting('canvas', 'scrolling_text', Bscrolling)
            self.main.modfy_setting('barrage', 'name', Bname)
            self.main.modfy_setting('barrage', 'size', Bsize)
            self.main.modfy_setting('barrage', 'alive_time', Btime)
            self.main.modfy_setting('barrage', 'alpha', Balpha)
        except Exception as e:
            logging.warning('save setting.ini failed.')
            logging.error(e)
            return
        save_ini('./setting.ini', self.main.setting)

    def btn_re_exec(self):
        logging.info('btn_re_exec clicked')
        os.startfile(sys.argv[0])
        self.main.close()

    def combo_platform(self):
        logging.info('combo_platform selected')
        index = self.main.ui.combo_platform.currentIndex()
        if index == 2:
            self.main.ui.edit_channel.setPlaceholderText("video ID")
            self.main.ui.edit_channel.setText('')
        else:
            self.main.ui.edit_channel.setPlaceholderText("channel")
            bot_platform = platform_list[index]
            channel = self.main.from_setting(bot_platform, 'channel', 'str')
            self.main.ui.edit_channel.setText(channel)

    def cb_optional(self):
        logging.info('cb_optional checked')
        check = self.main.ui.cb_optional.isChecked()
        if check:
            self.main.resize(700, 600)
        else:
            self.main.resize(400, 600)

    def cb_on_top(self):
        logging.info('cb_on_top checked')
        check = self.main.ui.cb_on_top.isChecked()
        self.main.modfy_setting('canvas', 'cover', check)
        if check:
            self.main.canvas.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.BypassWindowManagerHint | QtCore.Qt.WindowStaysOnTopHint)
            self.main.canvas.show()
            self.main.setFocus()
        else:
            self.main.canvas.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.BypassWindowManagerHint)
            self.main.canvas.show()
            self.main.setFocus()

    def cb_show_name(self):
        logging.info('cb_on_top checked')
        check = self.main.ui.cb_show_name.isChecked()
        self.main.modfy_setting('barrage', 'name', check)
        self.main.canvas.set_name_mode(check)

    def cb_avoid_crosshair(self):
        logging.info('cb_avoid_crosshair checked')
        check = self.main.ui.cb_avoid_crosshair.isChecked()
        self.main.modfy_setting('canvas', 'avoid_crosshair', check)
        self.main.barrage_thread.avoid_crosshair(check)

    def sli_alpha(self):
        # logging.info('sli_alpha changed')
        value = self.main.ui.sli_alpha.value()
        self.main.modfy_setting('barrage', 'alpha', value)
        self.main.canvas.set_alpha(value)