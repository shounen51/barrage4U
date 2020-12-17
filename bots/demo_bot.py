import logging
import threading
import time
import random

from configs import platform_list
from secret.bot_secret import discord_token

chats = {
    'fu6kme_':'666666',
    'lsls8787':'都看到一堆手電筒了還選隱鬼是斗M喔',
    'Km55489':'我不喜歡吃苦瓜',
    'Eeggggg0':'66666666',
    '溫蒂':'我叫我阿嬤來打都比你強，而且她已經過世了',
    '散步牛奶':'帶手電筒跟著鬼跑的都小王八蛋',
    'mad_Steve':'What\'s this game?',
    '魔法阿公':'苦瓜是歷史的罪人',
    'yukiko88':'請問小屋到底要怎麼追人？',
    '東亞病夫':'這個不修機的在幹嘛啦',
    'ssgew859':'?????',
    'james9576':'我每次鋼筋鐵骨都會被吃掉',
    '看衰仔':'這場應該四殺',
    'labmen007':'ZZZZZZZ'
}
class demo_bot(threading.Thread):
    platform = platform_list[0]
    title_tag = '@title'
    def __init__(self, main, args):
        super().__init__()
        self.main = main
        self.channel = args['channel']
        self.texts = {}
        self.EMOTE_MODE = self.main.from_setting(self.platform, 'emote', 'bool')
        self.TAKING = False
        self.TOKEN = discord_token
        self.BUSY = False
        self.go = True

    def login_and_run(self):
        self.start()

    def run(self):
        self.texts[self.title_tag] = ['已成功連結']
        # self.main.set_platform_when_logining(self.platform)
        self.main.ui.bot_login_signal.click()
        logging.info('Logged on demo')
        while self.go:
            for name in chats:
                self.texts[name] = [chats[name]]
                time.sleep(random.random() + 1)

    def fetch_text(self):
        _list = self.texts
        self.TAKING = True
        self.texts = {}
        self.TAKING = False
        return _list

    def too_busy(self):
        self.BUSY = True
        logging.info('bot is busy now.')

    def close(self):
        self.go = False
        self.join()

