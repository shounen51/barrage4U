import threading
import time
import math
import logging

from utils.barrage_class import barrage
from PyQt5.QtCore import QThread, pyqtSignal
import PyQt5.sip
import win32api

class scrolling_text_barrage(dict):
    def __init__(self, from_setting, canvas):
        super().__init__()
        self.from_setting = from_setting
        self.canvas = canvas
        self.BARRAGE_TAIL = 300
        self.BARRAGE_ALIVE_TIME = self.from_setting('barrage' ,'alive_time', 'int')
        self.fps = self.from_setting('canvas' ,'fps', 'int')
        self.ROLLING = False
        self.label = None

    def __new_barrage(self):
        w, h = self.canvas.get_text_w_h_with_emote(self['texts'])
        w += self.BARRAGE_TAIL
        x = self.canvas.width()
        y = int(self.canvas.height()-h)
        dis = ((x + w)/self.fps)/self.BARRAGE_ALIVE_TIME
        self['name'] = ''
        self['xywh'] = (x, y, w, h)
        self['dis'] = dis
        self['trajectory'] = -2

    def new(self):
        text = self.from_setting('canvas' ,'scrolling_text', 'str')
        if (not self.ROLLING) and text != '':
            self['texts'] = [text]
            self.ROLLING = True
            self.__new_barrage()
            return True
        else:
            return False

    def end(self):
        self.ROLLING = False

class Btype_CLASSIC_thread(QThread):
    new_signal = pyqtSignal(dict)
    move_signal = pyqtSignal(dict)
    def __init__(self, bot, canvas, main):
        super().__init__()
        self.bot = bot
        self.canvas = canvas
        self.main = main
        self.font_size = main.from_setting('barrage' ,'size', 'int')
        self.avoid_center = main.from_setting('canvas' ,'avoid_crosshair', 'bool')
        self.BARRAGE_ALIVE_TIME = main.from_setting('barrage' ,'alive_time', 'int')
        self.fps = main.from_setting('canvas' ,'fps', 'int')
        self.WORKING = False
        self.NEWING = False
        self.FIRST_ONE = 'init' # init, showing, over
        self.MAX_BARRAGE_IN_ONE_LINE = 20
        self.BARRAGE_TAIL = 301 # AN invisible tail of every barrage to make more space for each barrage in the same trajectory.
        self.next_Bid = 1
        self.font_h = 10
        self.texts_dict = {}
        self.barrages = {}
        self.new_barrages = {}
        self.title_barrage = {}
        self.scrolling_text_barrage = scrolling_text_barrage(self.main.from_setting, self.canvas)
        self.__count_trajectory_amont()
        self.trajectoris = [0 for _ in range(self.trajectory_amont)]
        if self.avoid_center:
            self.avoid_crosshair(True)


    def __count_trajectory_amont(self):
        if not self.WORKING:
            barrage_range = int(self.canvas.height()/5*4)
            self.canvas.set_font(size=self.font_size)
            _, self.font_h = self.canvas.get_text_w_h(".")
            self.trajectory_amont = int(barrage_range/self.font_h)
            return True
        else:
            return False

    # necessary
    def avoid_crosshair(self, avoid=True):
        crosshair = (win32api.GetSystemMetrics(0)/2, win32api.GetSystemMetrics(1)/2)
        t = int(crosshair[1]/self.font_h)
        if avoid:
            self.trajectoris[t] += self.MAX_BARRAGE_IN_ONE_LINE
            self.trajectoris[t+1] += self.MAX_BARRAGE_IN_ONE_LINE
        else:
            self.trajectoris[t] -= self.MAX_BARRAGE_IN_ONE_LINE
            self.trajectoris[t+1] -= self.MAX_BARRAGE_IN_ONE_LINE

    # necessary
    def start(self):
        self.WORKING = True
        super().start()

    def clear(self):
        self.stop()
        self.NEWING = False
        self.barrages.clear()
        self.new_barrages.clear()
        self.trajectoris.clear()
        self.trajectoris = [0 for _ in range(self.trajectory_amont)]

    # necessary
    def stop(self):
        self.WORKING = False
        super().terminate()

    def ui_new_label(self, _dict):
        Bid = self.next_Bid
        self.next_Bid += 1
        texts = _dict['texts']
        x, y, w, h = _dict['xywh']
        name = _dict['name']
        new_label = self.canvas.new_barrage_with_emote(Bid, name, texts, x, y, w, h, self.font_size)
        if _dict['trajectory'] == -1: # welcome
            self.title_barrage =  {
                'label' : new_label,
                'xywh' : _dict['xywh'],
                'trajectory' : -1,
                'st_time' : _dict['st_time'],
                'shooting' : True
            }
            self.FIRST_ONE = 'showing'
        else:
            self.new_barrages[str(Bid)] = {
                'label' : new_label,
                'xywh' : _dict['xywh'],
                'dis' : ((x + w)/self.fps)/self.BARRAGE_ALIVE_TIME,
                'trajectory' : _dict['trajectory'],
                'shooting' : True
            }

    def ui_move_label(self, _dict):
        label = _dict['label']
        x, y = _dict['xy']
        label.move(x, y)

    def __barrage_move(self):
        self.del_list = []
        if self.FIRST_ONE == 'showing':
            x, _, w, h = self.title_barrage['xywh']
            label = self.title_barrage['label']
            y = sigmoid_in_line_out(self.title_barrage['st_time'], h)
            self.move_signal.emit({
                    'label' : label,
                    'xy' : (x, y)
                })
            if (y + h) <= 0:
                self.FIRST_ONE = 'over'
                self.trajectoris[0] -= self.MAX_BARRAGE_IN_ONE_LINE
        for _id in self.barrages.keys():
            x, y, w, h = self.barrages[_id]['xywh']
            dis = self.barrages[_id]['dis']
            label = self.barrages[_id]['label']
            new_x = x - dis
            if new_x + w <= 0: #out of screen
                self.del_list.append(_id)
                if self.barrages[_id]['trajectory'] == -2:
                    self.scrolling_text_barrage.end()
            else:
                self.move_signal.emit({
                    'label' : label,
                    'xy' : (int(new_x), y)
                })
                self.barrages[_id]['xywh'] = (new_x, y, w, h)
                if self.barrages[_id]['shooting']:
                    if new_x + w < self.canvas.width():
                        trajectory = self.barrages[_id]['trajectory']
                        self.trajectoris[trajectory] -= 1
                        self.barrages[_id]['shooting'] = False

    def __barrage_del(self):
        for _id in self.del_list:
            self.barrages.pop(_id)
            self.canvas.del_barrage(int(_id))

    def __barrage_new(self, t1):
        while self.NEWING:
            time.sleep(0.001)
        self.barrages.update(self.new_barrages)
        self.new_barrages = {}
        self.texts_dict.update(self.bot.fetch_text())
        self.__make_rolling_text()
        while len(self.texts_dict) > 0 and time.time() - t1 < (1/self.fps):
            name = list(self.texts_dict.keys())[0]
            texts = self.texts_dict.pop(name)
            # drop new barrage if barrage is on limit.
            if not self.canvas.check_available_label():
                continue
            """find which trajectory to fire barrage"""
            if self.FIRST_ONE == 'init' and name == '@title':
                self.__make_title(texts)
            else:
                trajectory = -1
                for i in range(self.MAX_BARRAGE_IN_ONE_LINE):
                    if i in self.trajectoris:
                        trajectory = self.trajectoris.index(i)
                        self.trajectoris[trajectory] += 1
                        break
                if trajectory == -1:
                    continue

                w, h = self.canvas.get_text_w_h_with_emote(texts)
                w += self.BARRAGE_TAIL
                x = self.canvas.width()
                y = h * trajectory
                self.new_signal.emit({
                    'name' : name,
                    'texts' : texts,
                    'xywh' : (x,y,w,h),
                    'trajectory' : trajectory
                })

    def run(self):
        logging.info("barrage classic type on!")
        while self.WORKING:
            t1 = time.time()
            """move and del"""
            self.__barrage_move()
            self.__barrage_del()

            if time.time() - t1 > (1/self.fps):
                self.bot.too_busy()
                continue
            """new"""
            self.__barrage_new(t1)
            if time.time() - t1 < (1/self.fps):
                time.sleep((1/self.fps) - (time.time() - t1))
            else:
                self.bot.too_busy()

    def __make_title(self, texts):
        trajectory = -1
        self.trajectoris[0] += self.MAX_BARRAGE_IN_ONE_LINE
        w, h = self.canvas.get_text_w_h_with_emote(texts)
        st_time = time.time()
        x = int(((win32api.GetSystemMetrics(0)) - w) / 2)
        y = -h
        self.new_signal.emit({
            'name' : '',
            'texts' : texts,
            'xywh' : (x,y,w,h),
            'trajectory' : trajectory,
            'st_time': st_time
        })

    def __make_rolling_text(self):
        if self.scrolling_text_barrage.new():
            self.new_signal.emit(self.scrolling_text_barrage)

def sigmoid_in_line_out(st_time, height):
    x = time.time() - st_time
    if x < 6.5:
        # x*5 >> 約一秒到位， x >> 五秒到位
        y = (((1/(1+math.exp(-(x*5))))-0.5)*2)*height - height
    else:
        y = ((7-x)/0.5)*height - height
    return int(y)