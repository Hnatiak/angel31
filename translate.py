import types
import telebot
import config
import random
import logging
#import datetime
#from datetime import datetime
import time
#from telebot import types
#import sqlite3
#from sqlite3 import Error
from telebot import TeleBot, types

bot = telebot.TeleBot(config.TOKEN)


def translate_russian_to_ukrainian(word):
    translation_dict = {
        'спасиба': 'Дякую',
        'што': 'що',
        'шо': 'що',
        'что': 'що',
        'чо': 'що',
        'когда': 'коли',
        'как': 'як',
        'где': 'де',
        'но': 'але',
        'чиво': 'чого',
        'чево': 'чого',
        'чего': 'чого',
        'да': 'так',
        'нет': 'ні',
        'не': 'ні',
        'канеш': 'звісно',
        'канешно': 'звісно',
        'только': 'тільки/лише',
        'ладно': 'гаразд/окей',
        'ребят': 'друзі',
        'даровка': 'здоров',
        'даров': 'здоров',
        'хотел': 'здоров',
        'иди': 'йди/іди',
        'мать': 'мати',
        'почему': 'чому',
        'почти': 'майже',
        'тебе': 'тобі',
        'мне': 'мені',
        'ему': 'йому',
        # Додайте сюди інші слова та їх переклади
    }
    return translation_dict.get(word, word)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    words = re.findall(r'\b\w+\b', text)  # Знаходимо окремі слова в тексті

    for word in words:
        ukrainian_word = translate_russian_to_ukrainian(word)
        if word != ukrainian_word:
            reply = f"{word} немає в українській мові, правильно {ukrainian_word}"
            bot.reply_to(message, reply)
            break


bot.polling(none_stop=True)
