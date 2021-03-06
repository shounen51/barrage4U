# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import time
import ctypes
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw, ImageQt
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5.sip
import win32api

from configs import twitch_emote_url, platform_list
from ui.canvas_widgets import *
from utils.utils import image_RGBA_to_BGRA

class B_form(canvas_win):
    def __init__(self, from_setting):
        super().__init__()
        self.from_setting = from_setting
        self.font_size = self.from_setting('barrage', 'size', 'int')
        self.cover = self.from_setting('canvas', 'cover', 'bool')
        self.barrage_limit = self.from_setting('barrage', 'amont_limit', 'int')
        alpha = self.from_setting('barrage', 'alpha', 'int')
        self.NAMEMODE = self.from_setting('barrage', 'name', 'bool')
        self.alpha = int(255*(1-(alpha/100)))
        self.setWindowTitle("彈幕視窗")
        if self.cover:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.BypassWindowManagerHint | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.BypassWindowManagerHint)
        self.labels = []
        self.emotes = emotes()
        for i in range(self.barrage_limit):
            label = canvas_label(self)
            label.setGeometry(QtCore.QRect(win32api.GetSystemMetrics(0), 0, 0, 0))
            self.labels.append(label)
        self.labels_ids = [0 for _ in range(self.barrage_limit)]
        self.move(-2,-3)
        self.resize(win32api.GetSystemMetrics(0)+4, win32api.GetSystemMetrics(1)+5)
        self.font = QtGui.QFont('微軟正黑體', self.font_size)
        self.m = QtGui.QFontMetrics(self.font)
        _, self.h = self.get_text_w_h(".")


    def closeEvent(self, event):
        # self.__deleteItemsOfLayout()
        pass

    def set_font(self, font='微軟正黑體', size=36):
        self.font = QtGui.QFont(font, size)
        self.m = QtGui.QFontMetrics(self.font)

    def set_alpha(self, alpha):
        self.alpha = int(255*(1-(alpha/100)))

    def set_name_mode(self, NAMEMODE):
        self.NAMEMODE = NAMEMODE

    def check_available_label(self):
        if 0 in self.labels_ids:
            return True
        else:
            return False

    """ text only """
    def get_text_w_h(self, text):
        R = self.m.boundingRect(text)
        return int(R.width()*0.75)+10, R.height()

    def new_barrage(self, Bid, text, x, y, w, h, size=36):
        im = Image.new('RGBA', (w, h), (255, 255, 254, 0))
        font = ImageFont.truetype(
                "./fonts/msjh.ttc", size, encoding='utf-8')
        drawer = ImageDraw.Draw(im)
        fill_color = (255, 255, 254, self.alpha)
        stroke_color = (0, 0, 0, self.alpha)
        drawer.text((0, 0), text, font=font, fill=fill_color, stroke_width=1, stroke_fill=stroke_color)
        index = self.labels_ids.index(0)
        self.labels_ids[index] = Bid
        label = self.labels[index]
        label.setGeometry(QtCore.QRect(x, y, w, h))
        qim = QtGui.QImage(im.tobytes("raw","RGBA"), w, h, QtGui.QImage.Format_ARGB32)
        pix = QtGui.QPixmap.fromImage(qim)
        label.setPixmap(pix)
        return label

    """ with emote """
    def get_text_w_h_with_emote(self, words:list):
        length = 0
        _, h = self.get_text_w_h(".")
        for word in words:
            if word.startswith('http'):
                img = self.emotes.get_emotes(word)
                ratio = h/img.height
                w = int(img.width*ratio)
                length += w
            else:
                w, h = self.get_text_w_h(word)
                length += w
        return length + 2, h

    def new_barrage_with_emote(self, Bid, name, words:list, x, y, w, h, size=36):
        imgs = []
        if self.NAMEMODE and name != '':
            _w, _h = self.get_text_w_h(name)
            img = self._new_label_img(name, _w, _h, size, name=True)
            imgs.append(img)
            words.insert(0, ': ')
        for word in words:
            if not word.startswith('http'):
                _w, _h = self.get_text_w_h(word)
                img = self._new_label_img(word, _w, _h, size)
            else:
                img = self.emotes.get_emotes(word)
                ratio = self.h/img.height
                _w = int(img.width*ratio)
                img = img.resize((_w, h))
            imgs.append(img)
        img = self._concatenate_imgs(w, h, imgs)
        img = image_RGBA_to_BGRA(img)
        label = self._assign_label(Bid, x, y, w, h, img)
        return label

    def _new_label_img(self, text, w, h, size=36, name=False):
        im = Image.new('RGBA', (w, h), (255, 255, 254, 0))
        font = ImageFont.truetype(
                "./fonts/msjh.ttc", size, encoding='utf-8')
        drawer = ImageDraw.Draw(im)
        fill_color = (255, 255, 254, self.alpha) if not name else (204, 252, 255, self.alpha)
        stroke_color = (0, 0, 0, self.alpha)
        drawer.text((0, 0), text, font=font, fill=fill_color, stroke_width=1, stroke_fill=stroke_color)
        return im

    def _concatenate_imgs(self, w, h, imgs):
        c_img = Image.new('RGBA', (w, h), (255, 255, 254, 0))
        x = 0
        for img in imgs:
            c_img.paste(img, (x, 0))
            x += img.width
        return c_img

    def _assign_label(self, Bid, x, y, w, h, img):
        index = self.labels_ids.index(0)
        self.labels_ids[index] = Bid
        label = self.labels[index]
        label.setGeometry(QtCore.QRect(x, y, w, h))
        qim = QtGui.QImage(img.tobytes("raw","RGBA"), w, h, QtGui.QImage.Format_ARGB32)
        pix = QtGui.QPixmap.fromImage(qim)
        label.setPixmap(pix)
        return label

    def del_barrage(self, Bid):
        i = self.labels_ids.index(Bid)
        self.labels_ids[i] = 0

    def __deleteItemsOfLayout(self):
        if self is not None:
            while self.count():
                item = self.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    __deleteItemsOfLayout(item.layout())

class emotes():
    def __init__(self):
        self.platform = ""
        self.emotes = {}
    
    def set_platform(self, platform):
        self.platform = platform

    def get_emotes(self, url):
        #twitch
        if self.platform == platform_list[1]:
            if url in self.emotes:
                return self.emotes[url]
            else:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                self.emotes[url] = img
                return img
        #discord
        elif self.platform == platform_list[0]:
            if url in self.emotes:
                return self.emotes[url]
            else:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                self.emotes[url] = img
                return img
