import random
import re
import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

# def translate_russian_to_ukrainian(word):
#     translation_dict = {
#         'спасиба': 'Дякую',
#         'што': 'що',
#         'шо': 'що',
#         'что': 'що',
#         'чо': 'що',
#         'когда': 'коли',
#         'как': 'як',
#         'где': 'де',
#         'но': 'але',
#         'чиво': 'чого',
#         'чево': 'чого',
#         'чего': 'чого',
#         'да': 'так',
#         'нет': 'ні',
# #         'не': 'ні', ВИКЛЮЧЕННЯ
#         'канеш': 'звісно',
#         'канешно': 'звісно',
#         'только': 'тільки/лише',
#         'ладно': 'гаразд/окей',
#         'ребят': 'друзі',
#         'даровка': 'здоров',
#         'даров': 'здоров',
#         'хотел': 'здоров',
#         'иди': 'йди/іди',
#         'мать': 'мати',
#         'почему': 'чому',
#         'почти': 'майже',
#         'тебе': 'тобі',
#         'тебя': 'тебе',
#         'жёстко': 'жорстоко',
#         'мне': 'мені',
#         'ему': 'йому',
#         # Додайте сюди інші слова та їх переклади
#     }
#     return translation_dict.get(word, word)



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
        'да': 'так/та',
        'нет': 'ні',
#         'не': 'ні', ВИКЛЮЧЕННЯ
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
#         'тебе': 'тобі', ВИКЛЮЧЕННЯ
        'тебя': 'тебе',
        'жёстко': 'жорстоко',
        'мне': 'мені',
        'ему': 'йому',
        'меня': 'мене',
        'ты': 'ти',
        'бистро': 'швидко',
        'спасибо': 'дякую',
        # Додайте сюди інші слова та їх переклади
    }
    return translation_dict.get(word, word)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    words = re.findall(r'\b\w+\b', text)  # Знаходимо окремі слова в тексті

    translated_words = []
    for word in words:
        ukrainian_word = translate_russian_to_ukrainian(word)
        if word != ukrainian_word:
            translated_words.append((word, ukrainian_word))

    if translated_words:
        reply = ""
        for word_pair in translated_words:
            reply += f"{word_pair[0]}"
        reply += "немає в українській мові, правильно "
        for word_pair in translated_words:
            reply += f"{word_pair[1]} "
        bot.reply_to(message, reply)

# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     text = message.text.lower()
#     words = re.findall(r'\b\w+\b', text)  # Знаходимо окремі слова в тексті

#     for word in words:
#         ukrainian_word = translate_russian_to_ukrainian(word)
#         if word != ukrainian_word:
#             reply = f"{word} немає в українській мові, правильно {ukrainian_word}"
#             bot.reply_to(message, reply)
#             break


bot.polling(none_stop=True)
