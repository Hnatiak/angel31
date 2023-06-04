import random
import re
import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

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
        
        
        
        

#         'мы': 'ми',
#         'ничего': 'нічого',
#         'от': 'від/з',
#         'сложный': 'важкий',
#         'вопрос': 'питання/запитання',
#         'ещё': 'ще',
    }
    return translation_dict.get(word, word)

@bot.message_handler(func=lambda message: True)
def handle_message(bot, message):
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
            reply += f"{word_pair[0]}, "
        reply += "немає в українській мові, правильно "
        for word_pair in translated_words:
            reply += f"{word_pair[1]} "
        bot.reply_to(message, reply)



# import random
# import re
# import telebot
# import config

# bot = telebot.TeleBot(config.TOKEN)

# # Dictionary to store players' scores
# player_scores = {}

# # Number of points required to complete a quest
# QUEST_THRESHOLD = 1000

# def translate_russian_to_ukrainian(word):
#     translation_dict = {
#         # Translation mappings...
#     }
#     return translation_dict.get(word, word)

# @bot.message_handler(commands=['українські_бали'])
# def handle_ukrainian_scores_command(message):
#     table = "Учасники\n\n"
#     for player, score_data in player_scores.items():
#         name = score_data['name']
#         score = score_data['score']
#         quests = score_data['quests']
#         table += f"{name} {score} {quests} виконаних квестів\n"

#     bot.reply_to(message, table)

# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     text = message.text.lower()
#     words = re.findall(r'\b\w+\b', text)

#     # Get the player's score or initialize it if they are new
#     player_id = message.from_user.id
#     if player_id not in player_scores:
#         player_scores[player_id] = {
#             'name': message.from_user.username or message.from_user.first_name,
#             'score': 0,
#             'quests': 0
#         }
#     player_score = player_scores[player_id]['score']

#     ukrainian_words = 0
#     russian_words = 0

#     for word in words:
#         ukrainian_word = translate_russian_to_ukrainian(word)
#         if word != ukrainian_word:
#             if ukrainian_word in words:
#                 player_score -= 1
#             else:
#                 player_score += 1
#             ukrainian_words += 1
#         else:
#             russian_words += 1
#             player_score -= 1

#     # Update the player's score
#     player_scores[player_id]['score'] = player_score

#     # Check if the player has completed a quest
#     if player_score >= QUEST_THRESHOLD:
#         player_scores[player_id]['quests'] += 1
#         player_scores[player_id]['score'] = 0

#     # Send a reply with the player's score change
#     reply = f"Твій баланс: {player_score} (+{ukrainian_words}, -{russian_words})"
#     bot.reply_to(message, reply)

# bot.polling()


# import random
# import re
# import telebot
# import config

# bot = telebot.TeleBot(config.TOKEN)

# # Dictionary to store players' scores
# player_scores = {}

# # Number of points required to complete a quest
# QUEST_THRESHOLD = 1000

# def translate_russian_to_ukrainian(word):
#     translation_dict = {
#         # # А
    
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
#     }
#     return translation_dict.get(word, word)

# @bot.message_handler(commands=['українські_бали'])
# def handle_ukrainian_scores_command(message):
#     table = "Учасники\n\n"
#     for player, score_data in player_scores.items():
#         name = score_data['name']
#         score = score_data['score']
#         quests = score_data['quests']
#         table += f"{name} {score} {quests} виконаних квестів\n"

#     bot.reply_to(message, table)

# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     text = message.text.lower()
    
#     # Remove symbols and extra spaces from the message
#     text = re.sub(r'[^\w\s]', '', text)
#     text = re.sub(r'\s+', ' ', text)

#     words = text.split()

#     # Get the player's score or initialize it if they are new
#     player_id = message.from_user.id
#     if player_id not in player_scores:
#         player_scores[player_id] = {
#             'name': message.from_user.username or message.from_user.first_name,
#             'score': 0,
#             'quests': 0
#         }
#     player_score = player_scores[player_id]['score']

#     if len(words) > 3:
#         ukrainian_words = 0
#         russian_words = 0

#         for word in words:
#             ukrainian_word = translate_russian_to_ukrainian(word)
#             if word != ukrainian_word:
#                 if ukrainian_word in words:
#                     player_score -= 1
#                 else:
#                     player_score += 1
#                 ukrainian_words += 1
#             else:
#                 russian_words += 1
#                 player_score -= 1

#         # Update the player's score
#         player_scores[player_id]['score'] = player_score

#         # Check if the player has completed a quest
#         if player_score >= QUEST_THRESHOLD:
#             player_scores[player_id]['quests'] += 1
#             player_scores[player_id]['score'] = 0

#         # Send a reply with the player's score change
#         if ukrainian_words > 0:
#             reply = f"Твій баланс: +{ukrainian_words}"
#         elif russian_words > 0:
#             reply = f"Твій баланс: -{russian_words}"
#         else:
#             reply = "Твій баланс не змінився"

#         bot.reply_to(message, reply)

# bot.polling()
