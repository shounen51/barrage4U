import logging
import threading
import time

from configs import platform_list
from secret.bot_secret import discord_token

chats = {
    'aaa':'666666'
}
class demo_bot(threading.Thread):
    platform = platform_list[0]
    title_tag = '@title'
    def __init__(self, main, channel):
        super().__init__()
        self.main = main
        self.channel = channel
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
                time.sleep(1)

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

