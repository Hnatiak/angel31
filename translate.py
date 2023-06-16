# import random
# import re
# import telebot
# import config

# bot = telebot.TeleBot(config.TOKEN)

# def translate_russian_to_ukrainian(word):
#     translation_dict = {
#         'ё': 'їо',
#         'ы': 'и',
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
#         'доброе': 'доброго',

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
#         'и': 'і',
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
#         'лан': 'гаразд/окей',
        
# # М
#         'мать': 'мати',
#         'меня': 'мене',
#         'мы': 'ми',
#         'мой': 'мій',
#         'мне': 'мені',
#         'молчи': 'мовчи',
        
        
# # Н
# #         'не': 'ні', ВИКЛЮЧЕННЯ
#         'нада': 'потрібно',
#         'надо': 'потрібно',
#         'немного': 'трохи/трішки',
#         'немножко': 'трішки/трошки',
#         'нет': 'ні/немає',
#         'ничего': 'нічого',
#         'но': 'але',
        
# # О
#         'от': 'від/з/ось',
        
# # П
#         'пашлі': 'пішли/ходи',
#         'получаеться': 'виходить/получається',
#         'понятно': 'зрозуміло',
#         'похож': 'похожий/схожий/подібний',
#         'почему': 'чому',
#         'почти': 'майже',
#         'пошел': 'пішов',
#         'писать': 'писати',
#         'привык': 'привик/звик',
#         'пригати': 'стрибати/скакати',
#         'придложенієм': 'пропозицією',
        

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
#         'утро': 'ранок', 
#         'утра': 'ранку', 

# # Ф
#         'франсузком': 'французькій',

# # Х
#         'хотел': 'здоров',
#         'хуйня': 'фігня',

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
#         'шучу': 'жартую',

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
        'ё': 'їо',
        'ы': 'и',
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
        'дать': 'дати',
        'дал': 'дав',
        'даров': 'здоров',
        'дарова': 'здоров',
        'даровка': 'здоров',
        'дырочки': 'дирочки',
        'дыра': 'дира/дирка',

# Е
        'ему': 'йому',
        'её': 'її',
        'если': 'якщо',
        'ещё': 'ще',
        'ето': 'це',
        'еж': 'їжак',
        'ежа': 'їжака',

# Є

# Ж
        'жёстко': 'жорстоко',

# З
        'зонтик': 'парасоля',
        'зонтик': 'парасоля',
        'здарова': 'здоров',
        'значит': 'значить/це означає',

# И
        'иди': 'йди/іди',
        'изнасиловал': 'зґвалтував',
        'изнасиловала': 'зґвалтувала',
        'изнасиловала': 'зґвалтувала',

# І
        'ічо': 'і що',

# Ї

# Й

# К
        'как': 'як',
        'канеш': 'звісно',
        'канешно': 'звісно',
        'конечно': 'звісно',
        'конешно': 'звісно',
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
#       'не': 'ні', ВИКЛЮЧЕННЯ
        'наконец-то': 'нарешті/накінець-то',
        'надо': 'потрібно',
        'немного': 'трохи/трішки',
        'немножко': 'трішки/трошки',
        'нет': 'ні/немає',
        'ничего': 'нічого',
        'но': 'але',
        
# О
        'от': 'від/з/ось',
        
# П
        'попробуем': 'спробуємо',
        'понятно': 'зрозуміло',
        'похож': 'похожий/схожий/подібний',
        'почему': 'чому',
        'почти': 'майже',
        'писать': 'писати',
        'привет': 'привіт',
        'привык': 'привик/звик',
        

# Р
        'работает': 'працює',
        'ребят': 'друзі',

# С
        'свой': 'свій',
        'сейчас': 'зараз / на даний момент',
        'сладкие': 'солодкі',
        'сладка': 'солодко',
        'сложный': 'важкий',
        'сложна': 'важка/важко',
        'спасиба': 'Дякую',
        'спасибо': 'дякую',
        'сделал': 'зробив',
        'сделала': 'зробила',
        'скучно': 'нудно',
        

# Т
        'такое': 'таке',
#       'тебе': 'тобі', ВИКЛЮЧЕННЯ
        'ты': 'ти',
        'тебя': 'тебе',
        'только': 'тільки/лише',
        'тяжело': 'важко/тяжко',

# У
#         'уже': 'вже', ВИНЯТОК
        'уверен': 'впевнений',
        'уверена': 'впевнена',

# Ф
        'франсузком': 'французькій',

# Х
        'хотел': 'хотів',
        'хотела': 'хотіла',

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

def handle_message(message):
    player_id = message.from_user.id
    player_name = message.from_user.first_name

    if player_id not in player_scores:
        player_scores[player_id] = {'score': 0, 'quests': 0}

    text = message.text.lower()
    words = re.findall(r'\b\w+\b', text)

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
            bot.send_message(message.chat.id, reply)
        else:
            player_scores[player_id]['score'] += 1

        for word in words:
            if 'ё' in word or 'ы' in word or 'э' in word:
                player_scores[player_id]['score'] -= 1

        if player_scores[player_id]['score'] >= QUEST_THRESHOLD:
            player_scores[player_id]['quests'] += 1
            player_scores[player_id]['score'] = 0

@bot.message_handler(commands=['українські_бали'])
def display_scores(message):
    sorted_players = sorted(player_scores.items(), key=lambda x: x[1]['score'], reverse=True)
    reply = "Рейтинг гравців:\n"
    for player_id, player in sorted_players:
        player_name = bot.get_chat_member(message.chat.id, player_id).user.first_name
        reply += f"{player_name} - {player['score']} {player['quests']} виконаних квестів\n"
    reply += "\nЯкщо ти новенький, тоді пропиши /українські_бали_правила і прочитай які умови і як в це грати"
    bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['українські_бали_правила'])
def display_rules(message):
    rules = "Правила гри:\n"
    rules += "1. Бали нараховуються за кожне правильне слово українською мовою.\n"
    rules += "2. За кожне слово, яке НЕ існує в українській мові, гравцю знімається 1 бал.\n"
    rules += "3. Якщо слово містить букви 'ё' або 'ы', гравцю також знімається 1 бал.\n"
    rules += "4. Після набору 1000 балів гравець отримує +1 виконаний квест, після чого його бали автоматично обнуляються, і все починається заново\n"
    rules += "5. Для того щоб переглянути скільки ти маєш балів просто пропиши /українські_бали\n"
    bot.send_message(message.chat.id, rules)

# @bot.message_handler(commands=['українські_бали'])
# def display_scores(message):
#     reply = "Учасники:\n\n"
#     sorted_players = sorted(player_scores.items(), key=lambda x: x[1]['score'], reverse=True)
#     for player_id, player in sorted_players:
#         player_name = bot.get_chat_member(message.chat.id, player_id).user.first_name
#         reply += f"{player_name} - {player['score']} {player['quests']} виконаних квестів\n"
#     reply += "\nЯкщо ти новенький, тоді пропиши /українські_бали_правила і прочитай які умови і як в це грати"
#     bot.send_message(message.chat.id, reply)

# @bot.message_handler(commands=['українські_бали_правила'])
# def display_rules(message):
#     rules = "Правила гри:\n"
#     rules += "1. Бали нараховуються за кожне правильне слово українською мовою.\n"
#     rules += "2. За кожне слово, яке НЕ існує в українській мові, гравцю знімається 1 бал.\n"
#     rules += "3. Якщо слово містить букви 'ё' або 'ы', гравцю також знімається 1 бал.\n"
#     rules += "4. Після набору 1000 балів гравець отримує +1 виконаний квест, після чого його бали автоматично обнуляються, і все починається заново\n"
#     rules += "5. Для того щоб переглянути скільки ти маєш балів просто пропиши /українські_бали\n"
#     bot.send_message(message.chat.id, rules)

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

#         # Перевірка наявності букв "ё" або "ы" э у слові
#         for word in words:
#             if 'ё' in word or 'ы' in word or 'э' in word:
#                 player_scores[player_id]['score'] -= 1

#         # Перевірка виконання квесту
#         if player_scores[player_id]['score'] >= QUEST_THRESHOLD:
#             player_scores[player_id]['quests'] += 1
#             player_scores[player_id]['score'] = 0

# bot.polling(none_stop=True)
