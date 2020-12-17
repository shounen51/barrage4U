import asyncio
import logging

from pytchat import LiveChatAsync
from concurrent.futures import CancelledError

from configs import platform_list


class youtube_bot():
    platform = platform_list[2]
    welcome = [""]
    title_tag = '@title'
    def __init__(self, main, args):
        self.main = main
        self.__fetch_channel(args['channel'])
        self.texts = {}
        self.TAKING = False
        self.READY = False

    def __fetch_channel(self, channel):
        temp = channel
        if '/' in channel:
            temp = channel.split('/')[-1]
            if '?' in temp:
                args = temp.split('?')[-1]
                args = args.split('&')
                for arg in args:
                    if arg.startswith('v='):
                        temp = arg.replace('v=','')
        self.channel = temp

    def login_and_run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connect())

    def close(self):
        pass

    async def connect(self):
        livechat = LiveChatAsync(self.channel, callback = self.event_message, interruptable = False)
        while livechat.is_alive():
            if not self.READY:
                logging.info('Logged on youtube ' + self.channel)
                self.texts[self.title_tag] = ["系統訊息：已連接youtube頻道"]
                self.READY = True
                self.main.set_platform_when_logining(self.platform)
                self.main.ui.bot_login_signal.click()
            await asyncio.sleep(3)

    #callback function is automatically called.
    async def event_message(self, chatdata):
        for c in chatdata.items:
            words = []
            words.append(c.message)
            while self.TAKING:
                pass
            self.texts[c.author.name] = words
            await chatdata.tick_async()

    def fetch_text(self):
        _list = self.texts
        self.TAKING = True
        self.texts = {}
        self.TAKING = False
        return _list

    def too_busy(self):
        logging.info('bot is busy now.')

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except CancelledError:
        pass