import logging

import discord

from configs import platform_list
from secret.bot_secret import discord_token
class discord_bot(discord.Client):
    platform = platform_list[0]
    title_tag = '@title'
    def __init__(self, main, channel):
        discord.Client.__init__(self)
        self.main = main
        self.channel = channel
        self.texts = {}
        self.EMOTE_MODE = self.main.from_setting(self.platform, 'emote', 'bool')
        self.TAKING = False
        self.TOKEN = discord_token
        self.BUSY = False

    def login_and_run(self):
        self.run(self.TOKEN)

    async def on_ready(self):
        self.texts[self.title_tag] = ['已成功連結到：' + self.channel]
        self.main.set_platform_when_logining(self.platform)
        self.main.ui.bot_login_signal.click()
        logging.info('Logged on discord ' + self.channel)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if str(message.channel) == self.channel:
            temp = str(message.author).split('#')
            author = "".join(temp[:-1])
            if "\n" in message.content:
                await message.channel.send("彈幕只能單行啦，87喔" + author)
            elif "http" in message.content:
                await message.channel.send(author + "，別用網址發彈幕好嗎？")
            else:
                words = []
                if not message.content == '':
                    words.append(message.content)
                if len(message.attachments) > 0 and self.EMOTE_MODE:
                    words.append(message.attachments[0].url)
                if len(words) > 0:
                    while self.TAKING:
                        pass
                    self.texts[author] = words

        elif str(message.channel).startswith("Direct Message"):
            await message.channel.send("使用上若有任何疑問請到 https://github.com/shounen51/barrage4U 詢問")

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
        pass
