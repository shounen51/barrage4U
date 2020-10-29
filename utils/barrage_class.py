import time

import win32api
import win32con
import win32gui



class barrage():
    def __init__(self, text, Btype = 0, color = win32api.RGB(254, 254, 254), img = "", args = {}):
        """[summary]
        Args:
            text (str): text
            Btype (int, optional): The type of barrage. Default is right to left. It will be used when you want to make different type on the screen.
            color (win32api.RGB, optional): Text color. Default is white. Don't use (255,255,255)
            img (unknow, optional): Maybe it will be done someday. Maybe use base64. Defaults to "".
            args (dict, optional): For different barrage_type to save some information they need. Defaults to {}.
        """
        self.type = Btype
        self.text = text
        self.color = color
        self.img = img
        self.args = args
        self.start_time = time.time()
        self.rect = (0,0,0,0)

    def get_text(self):
        return self.text

    def get_color(self):
        return self.color

    def get_rect(self):
        return self.rect

    def get_img(self):
        return self.img

    def set_args(self, args):
        self.args = args