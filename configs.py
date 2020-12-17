platform_list = ['discord', 'twitch', 'youtube', 'demo']
twitch_emote_url = 'https://static-cdn.jtvnw.net/emoticons/v1'
twitch_emote_list_url = 'https://api.twitchemotes.com/api/v4/channels'

default_setting = {
    'basic':{
        'auto_connect': 'False'
    },
    'connect':{
        'platform':'twitch'
    },
    'canvas':{
        'cover':'True',
        'avoid_crosshair':'True',
        'fps':'60',
        'scrolling_text':''
    },
    'barrage':{
        'size':'36',
        'alive_time':'12',
        'amont_limit':'200',
        'long_limit':'30',
        'alpha':'20',
        'name':'True',
        'font':'微軟正黑體 (未作用)' #not yat
    },
    'discord':{
        'server':'',
        'channel':'',
        'emote':'True'
    },
    'twitch':{
        'channel':'',
        'emote':'True',
        'channel_id':''
    },
    'youtube':{
        'channel':''
    },
    'demo':{
        'channel':''
    }
}

from bots.discord_bot import discord_bot
from bots.twitch_bot import twitch_bot
from bots.youtube_bot import youtube_bot
from bots.demo_bot import demo_bot
bot_list = [discord_bot, twitch_bot, youtube_bot, demo_bot]