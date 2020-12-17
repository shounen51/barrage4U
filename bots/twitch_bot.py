import random
import logging

from twitchio.ext import commands

from utils.utils import HTTP_request
from configs import platform_list, twitch_emote_list_url
from secret.bot_secret import twitch_client_id, twitch_irc_token, twitch_nick

class twitch_bot(commands.Bot):
    platform = platform_list[1]
    welcome = ["imGlitch 這裡是 #id 的頻道"]
    title_tag = '@title'
    def __init__(self, main, args):
        self.main = main
        self.channel = args['channel']
        self.TAKING = False
        self.READY = False
        self.EMOTE_MODE = self.main.from_setting(self.platform, 'emote', 'bool')
        self.channel_id = self.main.ui.edit_twitch_id.text()
        self.irc_token = twitch_irc_token
        self.client_id = twitch_client_id
        self.nick = twitch_nick
        self.texts = {}
        super().__init__(irc_token=self.irc_token, client_id=self.client_id, nick=self.nick, prefix='!',
                         initial_channels=[self.channel])
        self.emote_tabel = self.__get_twitch_emotes()

    def login_and_run(self):
        self.run()

    def close(self):
        pass

    def __get_twitch_emotes(self):
        url = twitch_emote_list_url + '/0' # twitch defult emote
        ok, _re = HTTP_request(url, _type='get')
        emotes = {}
        if ok:
            re_emotes = _re['emotes']
            for emote in re_emotes:
                emotes[emote['code']] = emote['id']
        if not self.channel_id in ['0','']:
            url = twitch_emote_list_url + '/' + self.channel_id # twitch defult emote
            ok, _re = HTTP_request(url, _type='get')
            if ok:
                self.main.modfy_setting('twitch', 'channel_id', self.channel_id)
                re_emotes = _re['emotes']
                for emote in re_emotes:
                    emotes[emote['code']] = emote['id']
        return emotes

    def __precess_text(self, text):
        words = text.split(" ")
        ed_words = []
        for i, word in enumerate(words):
            if word in self.emote_tabel:
                if self.EMOTE_MODE:
                    word = "##" + str(self.emote_tabel[word])
                    ed_words.append(word)
            else:
                ed_words.append(word)
        return ed_words

    # Events don't need decorators when subclassed
    async def event_ready(self):
        logging.info('Logged on twitch ' + self.channel)
        text = self.welcome[random.randint(0,len(self.welcome)-1)].replace('#id', self.channel)
        words = self.__precess_text(text)
        self.texts[self.title_tag] = words
        self.main.set_platform_when_logining(self.platform)
        self.main.ui.bot_login_signal.click()
        self.READY = True
        # self.join_channels('shounensh51')

    async def event_message(self, message):
        if not 'http' in message.content and self.READY:
            contexts = self.__precess_text(message.content)
            if len(contexts) > 0:
                words = []
                words += contexts
                while self.TAKING:
                    pass
                self.texts[message.author.name] = words
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

    def fetch_text(self):
        _dict = self.texts
        self.TAKING = True
        self.texts = {}
        self.TAKING = False
        return _dict

    def too_busy(self):
        logging.info('bot is busy now.')