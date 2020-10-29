import threading

from configs import bot_list, platform_list, twitch_emote_url

class bot_thread():
    def __init__(self, main, long_limit=15):
        self.main = main
        self.long_limit = long_limit
        self.main_ui = main.ui
        self.LOGIN = False
        self.bot_platform = ""
        self.text_list = []
        self.emote_list = []

    def login(self, bot_platform, bot_channel):
        if not self.LOGIN:
            self.bot = bot_list[platform_list.index(bot_platform)](self.main, bot_channel)
            self.bot_platform = bot_platform
            self.LOGIN = True
            self.t = threading.Thread(target=self.__bot_login__, )
            self.t.setDaemon(True)
            self.t.start()
            return True
        else:
            print('Already login.')
            return False

    def __bot_login__(self):
        self.bot.login_and_run()

    def close(self):
        if self.LOGIN:
            self.bot.close()
            self.LOGIN = False

    def too_busy(self):
        self.bot.too_busy()

    def fetch_text(self):
        if self.LOGIN:
            words_dict = self.bot.fetch_text()
            labels_dict = {}
            # discord
            if self.bot_platform == platform_list[0]:
                for name in words_dict.keys():
                    words = words_dict[name]
                    if self.count_length(words):
                        labels_dict[name] = words
            # twitch
            elif self.bot_platform == platform_list[1]:
                for name in words_dict.keys():
                    words = words_dict[name]
                    if self.count_length(words):
                        labels = []
                        for word in words:
                            if word.startswith("##"):
                                word = word.replace("##", "")
                                emote_url = twitch_emote_url + '/' + word + '/3.0'
                                labels.append(emote_url)
                            else:
                                labels.append(word)
                        labels_dict[name] = labels
            # youtube
            elif self.bot_platform == platform_list[2]:
                for name in words_dict.keys():
                    words = words_dict[name]
                    if self.count_length(words):
                        labels_dict[name] = words
            return labels_dict
        else:
            return {}

    def count_length(self, words):
        length = 0
        if self.bot_platform == platform_list[0]:
            for word in words:
                if word.startswith('http'):
                    continue
                length += len(word)
        elif self.bot_platform == platform_list[1]:
            for word in words:
                if word.startswith("##"):
                    length += 1
                else:
                    length += len(word)
        elif self.bot_platform == platform_list[2]:
            length += len(''.join(words))
        if length > self.long_limit:
            return False
        else:
            return True