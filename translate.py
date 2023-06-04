# import random
# import re
# import telebot
# import config

# bot = telebot.TeleBot(config.TOKEN)

# def translate_russian_to_ukrainian(word):
#     translation_dict = {
# # А
    
# # Б
#         'бистро': 'швидко',
#         'больше': 'більше',
#         'боюсь': 'боюся',
#         'бес': 'біс',
#         'бесит': 'бісить',
        
# # В
#         'вопрос': 'питання/запитання',
# # Г
#         'где': 'де',
#         'говоришь': 'говориш/кажеш/розмовляєш/спілкуєшся',

# # Ґ

# # Д
#         'да': 'так/та',
#         'даров': 'здоров',
#         'даровка': 'здоров',

# # Е
#         'ему': 'йому',
#         'её': 'її',
#         'если': 'якщо',
#         'ещё': 'ще',

# # Є

# # Ж
#         'жёстко': 'жорстоко',

# # З
#         'значит': 'значить/це означає',

# # И
#         'иди': 'йди/іди',

# # І

# # Ї

# # Й

# # К
#         'как': 'як',
#         'канеш': 'звісно',
#         'канешно': 'звісно',
#         'когда': 'коли',
#         'красивый': 'красивий',

# # Л
#         'ладно': 'гаразд/окей',
        
# # М
#         'мать': 'мати',
#         'меня': 'мене',
#         'мы': 'ми',
#         'мой': 'мій',
#         'мне': 'мені',
#         'молчи': 'мовчи',
        
        
# # Н
# #         'не': 'ні', ВИКЛЮЧЕННЯ
#         'надо': 'потрібно',
#         'немного': 'трохи/трішки',
#         'немножко': 'трішки/трошки',
#         'нет': 'ні/немає',
#         'ничего': 'нічого',
#         'но': 'але',
        
# # О
#         'от': 'від/з/ось',
        
# # П
#         'понятно': 'зрозуміло',
#         'похож': 'похожий/схожий/подібний',
#         'почему': 'чому',
#         'почти': 'майже',
#         'писать': 'писати',
#         'привык': 'привик/звик',
        

# # Р
#         'ребят': 'друзі',

# # С
#         'свой': 'свій',
#         'сейчас': 'зараз / на даний момент',
#         'сложный': 'важкий',
#         'спасиба': 'Дякую',
#         'спасибо': 'дякую',
        

# # Т
#         'такое': 'таке',
# #         'тебе': 'тобі', ВИКЛЮЧЕННЯ
#         'ты': 'ти',
#         'тебя': 'тебе',
#         'только': 'тільки/лише',
#         'тяжело': 'важко/тяжко',

# # У
# #         'уже': 'вже', ВИНЯТОК

# # Ф
#         'франсузком': 'французькій',

# # Х
#         'хотел': 'здоров',

# # Ц

# # Ч
#         'час': 'година',
#         'часов': 'годин',
#         'чево': 'чого',
#         'чего': 'чого',
#         'чиво': 'чого',
#         'чо': 'що/чого',
#         'что': 'що',

# # Ш
#         'шо': 'що',
#         'што': 'що',

# # Щ

# # Ь

# # Ю

# # Я
        
        
        
        

# #         'мы': 'ми',
# #         'ничего': 'нічого',
# #         'от': 'від/з',
# #         'сложный': 'важкий',
# #         'вопрос': 'питання/запитання',
# #         'ещё': 'ще',
#     }
#     return translation_dict.get(word, word)

# @bot.message_handler(func=lambda message: True)
# def handle_message(bot, message):
#     text = message.text.lower()
#     words = re.findall(r'\b\w+\b', text)  # Знаходимо окремі слова в тексті

#     translated_words = []
#     for word in words:
#         ukrainian_word = translate_russian_to_ukrainian(word)
#         if word != ukrainian_word:
#             translated_words.append((word, ukrainian_word))

#     if translated_words:
#         reply = ""
#         for word_pair in translated_words:
#             reply += f"{word_pair[0]}, "
#         reply += "немає в українській мові, правильно "
#         for word_pair in translated_words:
#             reply += f"{word_pair[1]} "
#         bot.reply_to(message, reply)


import random
import re
import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

player_scores = {}  # Словник для збереження балів гравців
QUEST_THRESHOLD = 1000  # Поріг для виконання квесту
MIN_WORDS_THRESHOLD = 3

def translate_russian_to_ukrainian(word):
    translation_dict = {
# А
    
# Б
        'бистро': 'швидко',
        'больше': 'більше',
        'боюсь': 'боюся',
        'бес': 'біс',
        'бесит': 'бісить',
        
# В
        'вопрос': 'питання/запитання',
# Г
        'где': 'де',
        'говоришь': 'говориш/кажеш/розмовляєш/спілкуєшся',

# Ґ

# Д
        'да': 'так/та',
        'даров': 'здоров',
        'даровка': 'здоров',

# Е
        'ему': 'йому',
        'её': 'її',
        'если': 'якщо',
        'ещё': 'ще',

# Є

# Ж
        'жёстко': 'жорстоко',

# З
        'значит': 'значить/це означає',

# И
        'иди': 'йди/іди',

# І

# Ї

# Й

# К
        'как': 'як',
        'канеш': 'звісно',
        'канешно': 'звісно',
        'когда': 'коли',
        'красивый': 'красивий',

# Л
        'ладно': 'гаразд/окей',
        
# М
        'мать': 'мати',
        'меня': 'мене',
        'мы': 'ми',
        'мой': 'мій',
        'мне': 'мені',
        'молчи': 'мовчи',
        
        
# Н
#         'не': 'ні', ВИКЛЮЧЕННЯ
        'надо': 'потрібно',
        'немного': 'трохи/трішки',
        'немножко': 'трішки/трошки',
        'нет': 'ні/немає',
        'ничего': 'нічого',
        'но': 'але',
        
# О
        'от': 'від/з/ось',
        
# П
        'понятно': 'зрозуміло',
        'похож': 'похожий/схожий/подібний',
        'почему': 'чому',
        'почти': 'майже',
        'писать': 'писати',
        'привык': 'привик/звик',
        

# Р
        'ребят': 'друзі',

# С
        'свой': 'свій',
        'сейчас': 'зараз / на даний момент',
        'сложный': 'важкий',
        'спасиба': 'Дякую',
        'спасибо': 'дякую',
        

# Т
        'такое': 'таке',
#         'тебе': 'тобі', ВИКЛЮЧЕННЯ
        'ты': 'ти',
        'тебя': 'тебе',
        'только': 'тільки/лише',
        'тяжело': 'важко/тяжко',

# У
#         'уже': 'вже', ВИНЯТОК

# Ф
        'франсузком': 'французькій',

# Х
        'хотел': 'здоров',

# Ц

# Ч
        'час': 'година',
        'часов': 'годин',
        'чево': 'чого',
        'чего': 'чого',
        'чиво': 'чого',
        'чо': 'що/чого',
        'что': 'що',

# Ш
        'шо': 'що',
        'што': 'що',

# Щ

# Ь

# Ю

# Я
    }
    return translation_dict.get(word, word)
@bot.message_handler(commands=['українські_бали'])
def display_scores(message):
    reply = "Учасники\n"
    for player_id, player in player_scores.items():
        player_name = bot.get_chat_member(message.chat.id, player_id).user.first_name
        reply += f"{player_name} - {player['score']} {player['quests']} виконаних квестів\n"
    bot.reply_to(message, reply)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    player_id = message.from_user.id  # Отримуємо ідентифікатор гравця
    player_name = message.from_user.first_name  # Отримуємо ім'я гравця

    if player_id not in player_scores:
        player_scores[player_id] = {'score': 0, 'quests': 0}  # Ініціалізуємо бали гравця

    text = message.text.lower()
    words = re.findall(r'\b\w+\b', text)  # Знаходимо окремі слова в тексті

    if len(words) > MIN_WORDS_THRESHOLD:
        translated_words = []
        for word in words:
            ukrainian_word = translate_russian_to_ukrainian(word)
            if word != ukrainian_word:
                translated_words.append((word, ukrainian_word))

        if translated_words:
            reply = ""
            for word_pair in translated_words:
                reply += f"{word_pair[0]}, "
            reply += "немає в українській мові, правильно "
            for word_pair in translated_words:
                reply += f"{word_pair[1]} "
                player_scores[player_id]['score'] -= 1
            bot.reply_to(message, reply)
        else:
            player_scores[player_id]['score'] += 1

        # Перевірка виконання квесту
        if player_scores[player_id]['score'] >= QUEST_THRESHOLD:
            player_scores[player_id]['quests'] += 1
            player_scores[player_id]['score'] = 0

bot.polling()


# @bot.message_handler(commands=['українські_бали'])
# def display_scores(message):
#     reply = "Учасники\n"
#     for player_id, player in player_scores.items():
#         player_name = bot.get_chat_member(message.chat.id, player_id).user.first_name
#         reply += f"{player_name} - {player['score']} {player['quests']} виконаних квестів\n"
#     bot.reply_to(message, reply)

# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     player_id = message.from_user.id  # Отримуємо ідентифікатор гравця
#     player_name = message.from_user.first_name  # Отримуємо ім'я гравця

#     if player_id not in player_scores:
#         player_scores[player_id] = {'score': 0, 'quests': 0}  # Ініціалізуємо бали гравця

#     text = message.text.lower()
#     words = re.findall(r'\b\w+\b', text)  # Знаходимо окремі слова в тексті

#     if len(words) > MIN_WORDS_THRESHOLD:
#         translated_words = []
#         for word in words:
#             ukrainian_word = translate_russian_to_ukrainian(word)
#             if word != ukrainian_word:
#                 translated_words.append((word, ukrainian_word))

#         if translated_words:
#             reply = ""
#             for word_pair in translated_words:
#                 reply += f"{word_pair[0]}, "
#             reply += "немає в українській мові, правильно "
#             for word_pair in translated_words:
#                 reply += f"{word_pair[1]} "
#                 player_scores[player_id]['score'] -= 1
#             bot.reply_to(message, reply)
#         else:
#             player_scores[player_id]['score'] += 1

#         # Перевірка виконання квесту
#         if player_scores[player_id]['score'] >= QUEST_THRESHOLD:
#             player_scores[player_id]['quests'] += 1
#             player_scores[player_id]['score'] = 0

# bot.polling()
