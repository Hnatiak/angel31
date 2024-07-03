# import re
# import telebot
# import config
# import random
# from pyaspeller import YandexSpeller

# bot = telebot.TeleBot(config.TOKEN)

# game_numbers = {}

# @bot.message_handler(commands=['гра_в_цифри'])
# def start_number_game(message):
#     user_id = message.from_user.id

#     if user_id in game_numbers:
#         bot.send_message(chat_id=message.chat.id, text='Ви вже граєте в гру. Спробуйте закінчити попередню гру, прописавши команду /закінчити_гру.')
#         return

#     game_numbers[user_id] = {
#         'number': random.randint(1, 100),
#         'attempts_left': None
#     }

#     bot.send_message(chat_id=message.chat.id, text='Гра "Вгадай число" розпочата. Вгадайте число від 1 до 100.')


# @bot.message_handler(commands=['гра_в_цифри_10', 'гра_в_цифри_9', 'гра_в_цифри_8', 'гра_в_цифри_7', 'гра_в_цифри_6', 'гра_в_цифри_5', 'гра_в_цифри_4', 'гра_в_цифри_3', 'гра_в_цифри_2', 'гра_в_цифри_1'])
# def start_number_game_with_attempts(message):
#     user_id = message.from_user.id

#     if user_id in game_numbers:
#         bot.send_message(chat_id=message.chat.id, text='Ви вже граєте в гру. Спробуйте закінчити попередню гру, прописавши команду /закінчити_гру.')
#         return

#     attempts_left = int(message.text.split('_')[-1])
#     if attempts_left < 1 or attempts_left > 10:
#         bot.send_message(chat_id=message.chat.id, text='Кількість спроб має бути від 1 до 10.')
#         return

#     game_numbers[user_id] = {
#         'number': random.randint(1, 100),
#         'attempts_left': attempts_left
#     }

#     bot.send_message(chat_id=message.chat.id, text=f'Гра "Вгадай число" розпочата. Вгадайте число від 1 до 100. У вас є {attempts_left} спроб.')


# @bot.message_handler(func=lambda message: message.text.isdigit())
# def guess_number(message):
#     user_id = message.from_user.id

#     if user_id not in game_numbers:
#         bot.send_message(chat_id=message.chat.id, text='Ви ще не почали гру. Почніть гру командою /гра_в_цифри або /гра_в_цифри_(число від 1 - 10 спроб).')
#         return

#     game = game_numbers[user_id]
#     number = game['number']
#     attempts_left = game['attempts_left']

#     guess = int(message.text)

#     if guess == number:
#         bot.send_message(chat_id=message.chat.id, text='Вітаю! Ви вгадали число!')
#         del game_numbers[user_id]
#     elif guess < number:
#         bot.send_message(chat_id=message.chat.id, text='Загадане число більше.')
#     else:
#         bot.send_message(chat_id=message.chat.id, text='Загадане число менше.')

#     if attempts_left is not None:
#         game['attempts_left'] -= 1
#         if game['attempts_left'] == 0:
#             bot.send_message(chat_id=message.chat.id, text=f'Гра закінчена. Ви вичерпали всі спроби. Загадане число було {number}.')
#             del game_numbers[user_id]
#         else:
#             bot.send_message(chat_id=message.chat.id, text=f'У вас залишилося {game["attempts_left"]} спроб.')


# @bot.message_handler(commands=['закінчити_гру_в_цифри'])
# def end_number_game(message):
#     user_id = message.from_user.id

#     if user_id in game_numbers:
#         del game_numbers[user_id]
#         bot.send_message(chat_id=message.chat.id, text='Гра була закінчена.')
#     else:
#         bot.send_message(chat_id=message.chat.id, text='Ви не брали участі в жодній грі.')



# ukrainian_alphabet = ['а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з', 'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о',
#                       'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ю', 'я']

# excluded_words = ['сука', 'стриптиз', 'секс']
# special_ukrainian_words = {
#     'окунь': 'н',
#     'еге': 'г'
# }

# not_correct_ukrainian_words = ['продек', 'пкопр', 'пкойцв', 'цушгк']

# pending_games = {}

# def is_ukrainian_word(word):
#     speller = YandexSpeller()
#     spelling = list(speller.spell(word))
#     return len(spelling) == 0 and len(word) > 1

# def is_not_correct_ukrainian_word(word):
#     return any(word.startswith(w) for w in not_correct_ukrainian_words)

# def get_next_letter(word):
#     if word in special_ukrainian_words:
#         return special_ukrainian_words[word]
#     return word[-1]

# @bot.message_handler(commands=['гра_в_слова'])
# def start_word_game(message):
#     chat_id = message.chat.id
#     if chat_id in pending_games:
#         bot.send_message(chat_id, 'Гра вже розпочата. Дочекайтеся своєї черги.')
#     else:
#         pending_games[chat_id] = {'current_letter': '', 'participants': [], 'used_words': set()}
#         random_letter = random.choice(ukrainian_alphabet)
#         pending_games[chat_id]['current_letter'] = random_letter
#         bot.send_message(chat_id, f'Гра в слова почата. Перше слово починається на букву "{random_letter.upper()}"')


# @bot.message_handler(func=lambda message: re.match(r'^[а-яіїєґ]+$', message.text, re.IGNORECASE) is not None)
# def play_word_game(message):
#     chat_id = message.chat.id
#     if chat_id not in pending_games:
#         return

#     current_game = pending_games[chat_id]
#     current_letter = current_game['current_letter']
#     word = message.text.lower()

#     if not current_letter or word.startswith(current_letter):
#         if not is_ukrainian_word(word) or is_not_correct_ukrainian_word(word):
#             bot.send_message(chat_id, 'Це слово не є українським або містить лише одну літеру. Введіть нове слово.')
#             return

#         if word not in current_game['used_words']:
#             current_game['current_letter'] = get_next_letter(word)
#             current_game['participants'].append((message.from_user.username, word))
#             current_game['used_words'].add(word)
#             bot.send_message(chat_id, f'Наступне слово повинно починатися на букву "{current_game["current_letter"].upper()}"')
#         else:
#             bot.send_message(chat_id, 'Це слово вже було використано. Введіть нове слово.')
#     else:
#         bot.send_message(chat_id, f'Слово повинно починатися на букву "{current_letter.upper()}"')


# @bot.message_handler(commands=['закінчити_гру_в_слова'])
# def end_word_game(message):
#     chat_id = message.chat.id
#     if chat_id not in pending_games:
#         bot.send_message(chat_id, 'Немає активної гри.')
#         return

#     current_game = pending_games.pop(chat_id)
#     participants = current_game['participants']
#     if len(participants) == 0:
#         bot.send_message(chat_id, 'Гра завершена. Немає учасників.')
#     else:
#         result = '\n'.join([f'@{username}: {word}' for username, word in participants])
#         bot.send_message(chat_id, 'Гра завершена. Ось список учасників та слів:')
#         bot.send_message(chat_id, result)




import telebot
import config
import random
import re
from pyaspeller import YandexSpeller

bot = telebot.TeleBot(config.TOKEN)

game_numbers = {}
pending_games = {}

ukrainian_alphabet = ['а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з', 'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ю', 'я']
excluded_words = ['сука', 'стриптиз', 'секс', "крп", "ой"]
special_ukrainian_words = {'окунь': 'н', 'еге': 'г'}
not_correct_ukrainian_words = ['продек', 'пкопр', 'пкойцв', 'цушгк']

def is_ukrainian_word(word):
    speller = YandexSpeller()
    spelling = list(speller.spell(word))
    return len(spelling) == 0 and len(word) > 1

def is_not_correct_ukrainian_word(word):
    return any(word.startswith(w) for w in not_correct_ukrainian_words)

def get_next_letter(word):
    if word in special_ukrainian_words:
        return special_ukrainian_words[word]
    return word[-1]

# Ігри з числами
def start_number_game(message):
    user_id = message.from_user.id
    if user_id in game_numbers:
        bot.send_message(chat_id=message.chat.id, text='Ви вже граєте в гру. Спробуйте закінчити попередню гру, прописавши команду /закінчити_гру.')
        return

    game_numbers[user_id] = {'number': random.randint(1, 100), 'attempts_left': None}
    bot.send_message(chat_id=message.chat.id, text='Гра "Вгадай число" розпочата. Вгадайте число від 1 до 100.')

def start_number_game_with_attempts(message):
    user_id = message.from_user.id
    if user_id in game_numbers:
        bot.send_message(chat_id=message.chat.id, text='Ви вже граєте в гру. Спробуйте закінчити попередню гру, прописавши команду /закінчити_гру.')
        return

    attempts_left = int(message.text.split('_')[-1])
    if attempts_left < 1 or attempts_left > 10:
        bot.send_message(chat_id=message.chat.id, text='Кількість спроб має бути від 1 до 10.')
        return

    game_numbers[user_id] = {'number': random.randint(1, 100), 'attempts_left': attempts_left}
    bot.send_message(chat_id=message.chat.id, text=f'Гра "Вгадай число" розпочата. Вгадайте число від 1 до 100. У вас є {attempts_left} спроб.')

def guess_number(message):
    user_id = message.from_user.id
    if user_id not in game_numbers:
        bot.send_message(chat_id=message.chat.id, text='Ви ще не почали гру. Почніть гру командою /гра_в_цифри або /гра_в_цифри_(число від 1 - 10 спроб).')
        return

    game = game_numbers[user_id]
    number = game['number']
    attempts_left = game['attempts_left']

    guess = int(message.text)
    if guess == number:
        bot.send_message(chat_id=message.chat.id, text='Вітаю! Ви вгадали число!')
        del game_numbers[user_id]
    elif guess < number:
        bot.send_message(chat_id=message.chat.id, text='Загадане число більше.')
    else:
        bot.send_message(chat_id=message.chat.id, text='Загадане число менше.')

    if attempts_left is not None:
        game['attempts_left'] -= 1
        if game['attempts_left'] == 0:
            bot.send_message(chat_id=message.chat.id, text=f'Гра закінчена. Ви вичерпали всі спроби. Загадане число було {number}.')
            del game_numbers[user_id]
        else:
            bot.send_message(chat_id=message.chat.id, text=f'У вас залишилося {game["attempts_left"]} спроб.')

def end_number_game(message):
    user_id = message.from_user.id
    if user_id in game_numbers:
        del game_numbers[user_id]
        bot.send_message(chat_id=message.chat.id, text='Гра була закінчена.')
    else:
        bot.send_message(chat_id=message.chat.id, text='Ви не брали участі в жодній грі.')


def start_word_game(message):
    chat_id = message.chat.id
    if chat_id in pending_games:
        bot.send_message(chat_id, 'Гра вже розпочата. Дочекайтеся своєї черги.')
    else:
        pending_games[chat_id] = {'current_letter': '', 'participants': [], 'used_words': set()}
        random_letter = random.choice(ukrainian_alphabet)
        pending_games[chat_id]['current_letter'] = random_letter
        bot.send_message(chat_id, f'Гра в слова почата. Перше слово починається на букву "{random_letter.upper()}"')

def play_word_game(message):
    chat_id = message.chat.id
    if chat_id not in pending_games:
        return

    current_game = pending_games[chat_id]
    current_letter = current_game['current_letter']
    word = message.text.lower()

    if not current_letter or word.startswith(current_letter):
        if not is_ukrainian_word(word) or is_not_correct_ukrainian_word(word):
            bot.send_message(chat_id, 'Це слово не є українським або містить лише одну літеру. Введіть нове слово.')
            return

        if word not in current_game['used_words']:
            current_game['current_letter'] = get_next_letter(word)
            current_game['participants'].append((message.from_user.username, word))
            current_game['used_words'].add(word)
            bot.send_message(chat_id, f'Наступне слово повинно починатися на букву "{current_game["current_letter"].upper()}"')
        else:
            bot.send_message(chat_id, 'Це слово вже було використано. Введіть нове слово.')
    else:
        bot.send_message(chat_id, f'Слово повинно починатися на букву "{current_letter.upper()}"')

def end_word_game(message):
    chat_id = message.chat.id
    if chat_id not in pending_games:
        bot.send_message(chat_id, 'Немає активної гри.')
        return

    current_game = pending_games.pop(chat_id)
    participants = current_game['participants']
    if len(participants) == 0:
        bot.send_message(chat_id, 'Гра завершена. Немає учасників.')
    else:
        result = '\n'.join([f'@{username}: {word}' for username, word in participants])
        bot.send_message(chat_id, 'Гра завершена. Ось список учасників та слів:')
        bot.send_message(chat_id, result)