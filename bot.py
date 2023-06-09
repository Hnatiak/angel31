# -*- coding: utf-8 -*-

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
#from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#from telegram.ext import CallbackContext
# from datetime import datetime, timedelta, time
# import time
from datetime import datetime, timedelta, time
#import json
import re
#import yagmail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import speakwithbot.communication as communication
# import translate
from langdetect import detect

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(config.TOKEN)

game_numbers = {}
battles = {}

@bot.message_handler(commands=['написати_власнику'])
def send_email(message):
    bot.send_message(message.chat.id, "Будь ласка введіть ваше повідомлення:")
    bot.register_next_step_handler(message, send_email_message)

def send_email_message(message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('romanhnatiak@gmail.com', config.email_password)
        to_email = 'romanhnatiak@gmail.com'
        subject = 'Повідомлення від користувача'
        email_text = f"Від: {message.from_user.username}\nСмс: {message.text}"
        message = 'Subject: {}\n\n{}'.format(subject, email_text)
        server.sendmail('angel31@gmail.com', to_email, message)
        server.quit()
        bot.send_message(message.chat.id, "Чудово, ваш лист надіслано!")
    except:
        bot.send_message(message.chat.id, "На жаль щось пішло не так, повторіть операцію пізніше.")



pending_friendships = {}
friendships = []
ukrainian_alphabet = ['а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з', 'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ю', 'я']

pending_games = {}

@bot.message_handler(commands=['гра_в_слова'])
def start_game(message):
    chat_id = message.chat.id
    if chat_id in pending_games:
        bot.send_message(chat_id, 'Гра вже розпочата. Дочекайтеся своєї черги.')
    else:
        pending_games[chat_id] = {'current_letter': '', 'participants': [], 'used_words': set()}
        random_letter = random.choice(ukrainian_alphabet)
        pending_games[chat_id]['current_letter'] = random_letter
        bot.send_message(chat_id, f'Гра в слова почата. Перше слово починається на букву "{random_letter.upper()}"')

@bot.message_handler(func=lambda message: message.text.isalpha() and len(message.text) == 1)
def play_game(message):
    chat_id = message.chat.id
    if chat_id not in pending_games:
        return

    current_game = pending_games[chat_id]
    current_letter = current_game['current_letter']
    word = message.text.lower()

    if not current_letter or word.startswith(current_letter):
        if word not in current_game['used_words']:
            current_game['current_letter'] = word[-1]
            current_game['participants'].append((message.from_user.username, word))
            current_game['used_words'].add(word)
            bot.send_message(chat_id, f'Наступне слово повинно починатися на букву "{word[-1].upper()}"')
        else:
            bot.send_message(chat_id, 'Це слово вже було використано. Введіть нове слово.')
    else:
        bot.send_message(chat_id, 'Слово не починається на потрібну букву. Спробуйте ще раз.')

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    chat_id = message.chat.id
    if chat_id in pending_games:
        if message.text.isdigit():
            bot.send_message(chat_id, 'Наразі триває гра в слова. Введіть слово, щоб грати.')
        else:
            bot.send_message(chat_id, 'Будь ласка, введіть число або почніть нову гру.')






# ukrainian_alphabet = ['а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з', 'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ю', 'я']

# pending_games = {}

# @bot.message_handler(commands=['гра_в_слова'])
# def start_game(message):
#     chat_id = message.chat.id
#     if chat_id in pending_games:
#         bot.send_message(chat_id, 'Гра вже розпочата. Дочекайтеся своєї черги.')
#     else:
#         pending_games[chat_id] = {'current_letter': '', 'participants': [], 'used_words': set()}
#         random_letter = random.choice(ukrainian_alphabet)
#         pending_games[chat_id]['current_letter'] = random_letter
#         bot.send_message(chat_id, f'Гра в слова почата. Перше слово починається на букву "{random_letter.upper()}"')

# @bot.message_handler(func=lambda message: message.text.isalpha() and len(message.text) == 1)
# def play_game(message):
#     chat_id = message.chat.id
#     if chat_id not in pending_games:
#         return

#     current_game = pending_games[chat_id]
#     current_letter = current_game['current_letter']
#     word = message.text.lower()

#     if not current_letter or word.startswith(current_letter):
#         if detect(word) == 'uk':
#             if word not in current_game['used_words']:
#                 current_game['current_letter'] = word[-1]
#                 current_game['participants'].append((message.from_user.username, word))
#                 current_game['used_words'].add(word)
#                 bot.send_message(chat_id, f'Наступне слово повинно починатися на букву "{word[-1].upper()}"')
#             else:
#                 bot.send_message(chat_id, 'Це слово вже було використано. Введіть нове слово.')
#         else:
#             bot.send_message(chat_id, 'Слово не належить українській мові. Введіть слово українською.')
#     else:
#         bot.send_message(chat_id, 'Слово не починається на потрібну букву. Спробуйте ще раз.')

# @bot.message_handler(func=lambda message: True)
# def handle_other_messages(message):
#     chat_id = message.chat.id
#     if chat_id in pending_games:
#         bot.send_message(chat_id, 'Наразі триває гра в слова. Зачекайте, поки поточна гра завершиться.')

@bot.message_handler(commands=['стосунки'])
def add_friend(message):
    user1_id = message.chat.id
    if len(message.text.split()) == 1:
        bot.send_message(user1_id, 'Будь ласка, введіть імя користувача, з яким хочете одружитися.')
        return
    user2_name = message.text.split()[1]
    if not user2_name.startswith('@'):
        bot.send_message(user1_id, 'Будь ласка, введіть імя користувача у форматі @username.')
        return
    user2_username = user2_name[1:]

    pending_friendships[user1_id] = {'username': user2_username, 'time': datetime.now(), 'user2_id': None}

    confirmation_message = f'{message.from_user.username} хоче бути разом з тобою назавжди, ти погодишся??'
    confirmation_markup = types.InlineKeyboardMarkup()
    confirmation_yes_button = types.InlineKeyboardButton('Yes',
                                                         callback_data=f'confirm_friendship:{user1_id}:{user2_username}:yes')
    confirmation_no_button = types.InlineKeyboardButton('No',
                                                        callback_data=f'confirm_friendship:{user1_id}:{user2_username}:no')
    confirmation_markup.add(confirmation_yes_button, confirmation_no_button)
    bot.send_message(message.chat.id, confirmation_message, reply_markup=confirmation_markup)


@bot.callback_query_handler(lambda query: query.data.startswith('confirm_friendship'))
def confirm_friendship(callback_query):
    # Get the IDs of the users involved in the friendship request
    user1_id = callback_query.message.chat.id
    user2_username = callback_query.data.split(':')[2]

    # Check if the friend request was sent less than 60 seconds ago
    if user1_id in pending_friendships and user2_username == pending_friendships[user1_id]['username'] \
            and (datetime.now() - pending_friendships[user1_id]['time']).total_seconds() < 60:

        if callback_query.data.endswith('yes'):
            print("Yes button clicked")  # add this line
            # Update the database to record the friendship
            user2_id = get_user_id_from_username(user2_username)
            if user2_id:
                friendships.append(
                    {'user1_id': user1_id, 'user2_id': user2_id, 'date': datetime.now(), 'confirmed': True})
                bot.send_message(user1_id, f"Твоя половинка {user2_username} підтвердив(-ла) твоє прохання!")
                bot.send_message(user2_id, f"Ти дружиш з {callback_query.from_user.username}!")
            else:
                bot.send_message(user1_id, f"Не вдалося знайти користувача з ім'ям {user2_username}.")
        else:
            bot.send_message(user1_id, f"Твоя половинка {user2_username} відхилив(-ла) твоє прохання.")

        del pending_friendships[user1_id]

    else:
        bot.send_message(user1_id, 'Вибачте, термін дії вашого запиту про дружби минув.')

#@bot.message_handler(commands=['мої_стосунки'])
#def show_friendship_date(message):
#    user_id = message.chat.id
#    # Check if there is a confirmed friendship involving the user
#    friendship_date = get_friendship_date(user_id)
#    if friendship_date:
#        bot.send_message(user_id, f"Ви разом вже з {friendship_date.strftime('%d.%m.%Y')}!")
#    else:
#        bot.send_message(user_id, "Ви ще не маєте підтверджених в стосунках.")
#
#def get_friendship_date(user_id):
    # Check the database for a confirmed friendship involving the user
    # Return the date of the friendship, or None if there is no confirmed friendship
    # ...
#    return datetime.now() # Placeholder value, replace with actual database lookup

#@bot.message_handler(commands=['розірвати_стосунки'])
#def remove_friendship(message):
#    user_id = message.chat.id
#    # Check if there is a confirmed friendship involving the user
#    if get_friendship_date(user_id):
#        # Update the database to remove the friendship
#        # ...
#
#        bot.send_message(user_id, "Ваші стосунки були розірвані.")
#    else:
#        bot.send_message(user_id, "Ви ще не маєте підтверджених в стосунках.")

#@bot.message_handler(commands=['мої_стосунки'])
#def show_friendship_date(message):
#    user_id = message.chat.id
#    # Check if there is a confirmed friendship involving the user
#    friendship_date = get_friendship_date(user_id)
#    if friendship_date:
#        bot.send_message(user_id, f"Ви дружите з {friendship_date.strftime('%d.%m.%Y %H:%M:%S')}.")
#    else:
#        bot.send_message(user_id, "Ви ще не в стосунках. Для того, щоб бути в стосунках, введіть /стосунки @імя_користувача.")


@bot.message_handler(commands=['мої_стосунки'])
def show_friendship_date(message):
    user_id = message.chat.id
    # Check if there is a confirmed friendship involving the user
    friendship_date = None
    for friendship in friendships:
        if friendship['user1_id'] == user_id and friendship['confirmed']:
            friendship_date = friendship['date']
            break
        elif friendship['user2_id'] == user_id and friendship['confirmed']:
            friendship_date = friendship['date']
            break
    if friendship_date:
        bot.send_message(user_id, f"Ви дружите з {friendship_date.strftime('%d.%m.%Y %H:%M:%S')}.")
    else:
        bot.send_message(user_id, "Ви ще не в стосунках. Для того, щоб бути в стосунках, введіть        /стосунки @імя_користувача.")

def get_friendship_date(user_id):
    # Check the database for a confirmed friendship involving the user
    # Return the date of the friendship, or None if there is no confirmed friendship
    # ...
    return datetime.now() # Placeholder value, replace with actual database lookup

@bot.message_handler(commands=['розірвати_стосунки'])
def remove_friendship(message):
    user_id = message.chat.id
    # Check if there is a confirmed friendship involving the user
    friendship_date = get_friendship_date(user_id)
    if friendship_date:
        # Update the database to remove the friendship
        # ...
        bot.send_message(user_id, "Ваші стосунки були розірвані.")
    else:
        bot.send_message(user_id, "Ви ще не в стосунках. Для того, щоб бути в стосунках, введіть /стосунки @імя_користувача.")


@bot.message_handler(commands=['help_bot', 'start'])
def greeting(message):
    bot.send_message(message.chat.id, "У мене доступні такі команди як:\n\n<b>/від вдарити</b>, \n<b>/від обняти</b>, "
                                      "\n<b>/від поцілувати</b> \n<b>/від образити</b>\n<b>/від чмок</b>\n<b>/від шльоп</b>"
                                      "\n<b>/від сильнийшльоп</b>\n<b>/від кекс або ж /від секс</b>\n<b>/від онанізм</b>"
                                      "\n<b>/від засос</b>\n<b>/стать</b>\n<b>Відповідати на запитання на скільки хтось розумний чи дурний</b>"
                                      "\n<b>Відповідати на запитання так чи ні (В кінці обовязково напиши ?, для прикладу: ангел таке можливе?)</b>"
                                      "\n\nТакож я маю звичайні команди як:\n\n<b>показати ніжки</b>\n\n<b>А також я можу надавати інформацію про те як купити "
                                      "піар або адмінку, просто пропиши: купити піар, або купити адмінку</b>\n\n Також у мене є ігри як:\n\n/гра_в_цифри", parse_mode='html', disable_web_page_preview=True)
    bot.send_photo(message.chat.id, open('static/01.jpg', 'rb'))


user_choices = {}

gender = ""


@bot.message_handler(commands=['гра_в_цифри'])
def start_number_game(message):
    user_id = message.from_user.id

    if user_id in game_numbers:
        bot.send_message(chat_id=message.chat.id, text='Ви вже граєте в гру. Спробуйте закінчити попередню гру, прописавши команду /закінчити_гру.')
        return

    game_numbers[user_id] = {
        'number': random.randint(1, 100),
        'attempts_left': None
    }

    bot.send_message(chat_id=message.chat.id, text='Гра "Вгадай число" розпочата. Вгадайте число від 1 до 100.')


@bot.message_handler(commands=['гра_в_цифри_10', 'гра_в_цифри_9', 'гра_в_цифри_8', 'гра_в_цифри_7', 'гра_в_цифри_6', 'гра_в_цифри_5', 'гра_в_цифри_4', 'гра_в_цифри_3', 'гра_в_цифри_2', 'гра_в_цифри_1'])
def start_number_game_with_attempts(message):
    user_id = message.from_user.id

    if user_id in game_numbers:
        bot.send_message(chat_id=message.chat.id, text='Ви вже граєте в гру. Спробуйте закінчити попередню гру, прописавши команду /закінчити_гру.')
        return

    attempts_left = int(message.text.split('_')[-1])
    if attempts_left < 1 or attempts_left > 10:
        bot.send_message(chat_id=message.chat.id, text='Кількість спроб має бути від 1 до 10.')
        return

    game_numbers[user_id] = {
        'number': random.randint(1, 100),
        'attempts_left': attempts_left
    }

    bot.send_message(chat_id=message.chat.id, text=f'Гра "Вгадай число" розпочата. Вгадайте число від 1 до 100. У вас є {attempts_left} спроб.')


@bot.message_handler(func=lambda message: message.text.isdigit())
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
            
            
            

# # Обробник команди /гра_в_цифри_батл
# @bot.message_handler(commands=['гра_в_цифри_батл'])
# def handle_battle_start(message):
#     chat_id = message.chat.id

#     # Перевіряємо, чи батл уже активний в даному чаті
#     if chat_id in battles:
#         bot.send_message(chat_id, 'Батл вже активний!')
#         return

#     # Створюємо клавіатуру з кнопкою "Прийняти батл"
#     markup = types.InlineKeyboardMarkup()
#     accept_button = types.InlineKeyboardButton(text='Прийняти батл', callback_data='прийняти_батл')
#     markup.add(accept_button)

#     # Надсилаємо повідомлення в груповий чат з кнопкою "Прийняти батл"
#     bot.send_message(chat_id, 'Хто готовий до батлу?', reply_markup=markup)

#     # Зберігаємо інформацію про батл
#     battles[chat_id] = {'players': [], 'accepted_players': []}

# # Обробник події кліку на кнопку "Прийняти батл"
# @bot.callback_query_handler(func=lambda call: call.data == 'прийняти_батл')
# def handle_battle_accept(call):
#     chat_id = call.message.chat.id
#     user_id = call.from_user.id

#     # Перевіряємо, чи батл активний в даному чаті
#     if chat_id not in battles:
#         bot.send_message(chat_id, 'Батл вже завершено!')
#         return

#     # Перевіряємо, чи гравець не прийняв батл раніше
#     if user_id in battles[chat_id]['accepted_players']:
#         bot.send_message(chat_id, 'Ви вже прийняли батл!')
#         return

#     # Додаємо гравця до списку прийнятих гравців
#     battles[chat_id]['accepted_players'].append(user_id)

#     # Перевіряємо, чи є ще мінімум два прийнятих гравці
#     if len(battles[chat_id]['accepted_players']) >= 2:
#         start_battle(chat_id)

# # Функція початку батлу
# def start_battle(chat_id):
#     # Видаляємо кнопку "Прийняти батл" з групового чату
#     bot.edit_message_reply_markup(chat_id, message_id=bot_message_id, reply_markup=None)

#     # Відправляємо приватне повідомлення обом гравцям
#     players = battles[chat_id]['accepted_players']
#     for player in players:
#         bot.send_message(player, 'Загадайте будь-яке число від 1 до 100')

# # Обробник приватного повідомлення з загаданим числом
# @bot.message_handler(func=lambda message: message.chat.type == 'private')
# def handle_private_message(message):
#     user_id = message.from_user.id
#     chat_id = message.chat.id

#     # Перевіряємо, чи є гравець у списку прийнятих гравців
#     if chat_id not in battles or user_id not in battles[chat_id]['accepted_players']:
#         bot.send_message(user_id, 'Ви не можете грати у батл!')

#     # Отримуємо загадане число гравця
#     guessed_number = int(message.text)

#     # Отримуємо числа других гравців
#     other_players = [player for player in battles[chat_id]['accepted_players'] if player != user_id]

#     # Вгадуємо числа других гравців
#     for player in other_players:
#         opponent_number = random.randint(1, 100)

#         # Порівнюємо числа і визначаємо переможця
#         if opponent_number == guessed_number:
#             bot.send_message(chat_id, f"Гравець {user_id} вгадав число противника {opponent_number}. Вітаємо з перемогою!")
#         elif abs(opponent_number - guessed_number) < abs(guessed_number - opponent_number):
#             bot.send_message(chat_id, f"Гравець {user_id} наблизився до числа противника {opponent_number}.")
#         else:
#             bot.send_message(chat_id, f"Гравець {user_id} віддалився від числа противника {opponent_number}.")


# @bot.message_handler(commands=['закінчити_батл'])
# def end_battle(message):
#     user_id = message.from_user.id

#     if user_id not in battles:
#         bot.send_message(chat_id=message.chat.id, text='Ви не берете участі в батлі. Почніть новий батл, прописавши команду /гра_в_цифри_батл.')
#         return

#     opponent_id = None
#     if battles[user_id]['challenger'] == user_id:
#         opponent_id = battles[user_id]['opponent']
#     elif battles[user_id]['opponent'] == user_id:
#         opponent_id = battles[user_id]['challenger']

#     del battles[user_id]

#     if opponent_id is not None:
#         bot.send_message(chat_id=opponent_id, text='Ваш противник вийшов з батлу. Батл завершено.')


@bot.message_handler(commands=['закінчити_гру'])
def end_number_game(message):
    user_id = message.from_user.id

    if user_id in game_numbers:
        del game_numbers[user_id]
        bot.send_message(chat_id=message.chat.id, text='Гра була закінчена.')
    else:
        bot.send_message(chat_id=message.chat.id, text='Ви не брали участі в жодній грі.')


@bot.message_handler(commands=['стать'])
def handle_gender_choice(message):
    user_id = message.from_user.id
    if user_choices.get(user_id) is not None:
        bot.send_message(chat_id=message.chat.id, text='Ваша стать уже була обрана, для того щоб її змінити пропишіть /змінити_стать, якщо ти хочеш переглянути свою стать то пропиши /моя_стать')
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    male_button = types.InlineKeyboardButton(text='Чоловіча', callback_data='Чоловіча')
    female_button = types.InlineKeyboardButton(text='Жіноча', callback_data='Жіноча')
    markup.add(male_button, female_button)
    bot.send_message(chat_id=message.chat.id, text='Виберіть свою стать:', reply_markup=markup)
    user_choices[user_id] = None


@bot.callback_query_handler(func=lambda call: True)
def handle_gender_callback(call):
    user_id = call.from_user.id
    if user_choices.get(user_id) is not None:
        bot.send_message(chat_id=call.message.chat.id, text='Ваша стать уже була обрана, для того щоб її змінити пропишіть /змінити_стать')
        return
    user_choices[user_id] = call.data
    if call.data == 'Чоловіча':
        bot.send_message(chat_id=call.message.chat.id, text='Ваша стать обрана: Чоловіча')
    elif call.data == 'Жіноча':
        bot.send_message(chat_id=call.message.chat.id, text='Ваша стать обрана: Жіноча')


@bot.message_handler(commands=['змінити_стать'])
def handle_change_gender(message):
    user_id = message.from_user.id
    user_choices[user_id] = None
    markup = types.InlineKeyboardMarkup(row_width=2)
    male_button = types.InlineKeyboardButton(text='Чоловіча', callback_data='Чоловіча')
    female_button = types.InlineKeyboardButton(text='Жіноча', callback_data='Жіноча')
    markup.add(male_button, female_button)
    bot.send_message(chat_id=message.chat.id, text='Виберіть свою стать:', reply_markup=markup)

@bot.message_handler(commands=['моя_стать'])
def handle_gender(message):
    user_id = message.from_user.id
    gender = user_choices.get(user_id)
    if gender is not None:
        bot.send_message(chat_id=message.chat.id, text=f'Ваша стать обрана: {gender}')
    else:
        bot.send_message(chat_id=message.chat.id, text='Ви ще не обрали свою стать, для того щоб її обрати пропишіть    /стать')


@bot.message_handler(commands=['від'])
def hug_or_kiss(message):
    words = message.text.lower().split()
    if len(words) < 2:
        bot.reply_to(message, "Виберіть дію щоб виконати цю команду")
    else:
        action = words[1]
        target = message.reply_to_message.from_user if message.reply_to_message else None
        if not target:
            bot.reply_to(message, "Виберіть користувача щоб виконати цю команду")
            return
        reply_user = message.reply_to_message.from_user
        action = message.text.split(' ')[1].lower()
        reason = ' '.join(message.text.split(' ')[2:]) if len(message.text.split(' ')) > 2 else ''
        if action == 'обняти':
            bot.send_message(message.chat.id, f"😘 {message.from_user.first_name} обняв(-ла) {reply_user.first_name}\n{reason}")
            photo_choices = ['static/hugs/hugs_one.jpg', 'static/hugs/hugs_two.jpg', 'static/hugs/hugs_three.jpg',
                             'static/hugs/hugs_four.jpg', 'static/hugs/hugs_five.jpg', 'static/hugs/hugs_six.jpg',
                             'static/hugs/hugs_seven.jpg', 'static/hugs/hugs_eight.jpg', 'static/hugs/hugs_nine.jpg',
                             'static/hugs/hugs_ten.jpg']
        elif action == 'поцілувати':
            bot.send_message(message.chat.id, f" 😘 {message.from_user.first_name} поцілував(-ла) {reply_user.first_name}\n{reason}")
            photo_choices = ['static/kisses/kiss_one.jpg', 'static/kisses/kiss_two.jpg', 'static/kisses/kiss_three.jpg',
                             'static/kisses/kiss_four.jpg', 'static/kisses/kiss_one.jpg', 'static/kisses/kiss_five.jpg',
                             'static/kisses/kiss_six.jpg', 'static/kisses/kiss_seven.jpg', 'static/kisses/kiss_one.gif']
        elif action == 'вдарити':
            bot.send_message(message.chat.id, f" 🤜🤕 {message.from_user.first_name} вдарив(-ла) {reply_user.first_name}\n{reason}")
            photo_choices = ['static/bully/bully_one.gif', 'static/bully/bully_two.gif', 'static/bully/bully_three.gif',
                             'static/bully/bully_four.gif', 'static/bully/bully_five.gif', 'static/bully/bully_six.gif',
                             'static/bully/bully_seven.gif', 'static/bully/bully_eight.gif', 'static/bully/bully_nine.gif'
                             'static/bully/bully_ten.gif']
        elif action == 'образити':
            bot.send_message(message.chat.id, f"😒 {message.from_user.first_name} образив(-ла) {reply_user.first_name}\nПричина: {reason}")
            photo_choices = []
        elif action in ['потиснути руку', 'пожати руку', 'пожати']:
            bot.send_message(message.chat.id, f"🤗 {message.from_user.first_name} пожав руку {reply_user.first_name}\n{reason}")
            photo_choices = []
        elif action == 'чмок':
            bot.send_message(message.chat.id, f"🤗 {message.from_user.first_name} чмокнув(-ла) {reply_user.first_name}\n{reason}")
            photo_choices = ['static/kisses/kiss_one.jpg', 'static/kisses/kiss_two.jpg', 'static/kisses/kiss_three.jpg', 'static/kisses/kiss_four.jpg', 'static/kisses/kiss_one.jpg', 'static/kisses/kiss_five.jpg', 'static/kisses/kiss_six.jpg', 'static/kisses/kiss_seven.jpg']
        elif action == 'шльоп':
            bot.send_message(message.chat.id, f"🤗 {message.from_user.first_name} шльопнув(-ла) {reply_user.first_name} і він/вона попросив(-ла) ще сильніше")
            photo_choices = ['static/slaps/slap_one.gif', 'static/slaps/slap_two.gif', 'static/slaps/slap_three.gif', 'static/slaps/slap_four.gif']
        elif action == 'сильнийшльоп':
            bot.send_message(message.chat.id, f"🤗 {message.from_user.first_name} зі всієї дурі шльопнув(-ла) {reply_user.first_name} і вона досягла оргазму 🤤")
            photo_choices = ['static/slaps/slap_one.gif', 'static/slaps/slap_two.gif', 'static/slaps/slap_three.gif', 'static/slaps/slap_four.gif']
        elif action in ('кекс', 'секс'):
            bot.send_message(message.chat.id, f"🥵😫 {message.from_user.first_name} трахнув(-ла) {reply_user.first_name}\n{reason}")
            photo_choices = ['static/se/se_one.gif', 'static/se/se_two.gif']
        elif action == 'засос':
            bot.send_message(message.chat.id, f"🥵 {message.from_user.first_name} зацілував(-ла) свою половинку {reply_user.first_name}")
            photo_choices = ['static/strong_kiss/strong_kiss_one.gif', 'static/strong_kiss/strong_kiss_two.gif', 'static/strong_kiss/strong_kiss_three.webp']
        elif action == 'шури-мури':
            bot.send_message(message.chat.id, f"🤭 {message.from_user.first_name} пошури-мурив(-ла) {reply_user.first_name}")
            photo_choices = []
        elif action == 'відрізати':
            bot.send_message(message.chat.id, f"🤭 {message.from_user.first_name} відрізав(-ла) {reply_user.first_name}")
            photo_choices = []
        elif action == 'вдочерити':
            bot.send_message(message.chat.id, f"🤗 {message.from_user.first_name} вдочерив(-ла) {reply_user.first_name}\n{reason}")
            photo_choices = ['static/ideas/ideas_one.gif']
        elif action == 'онанізм':
            bot.send_message(message.chat.id, f"🥵 {message.from_user.first_name} зайнявся(-лася) самозадоволенням\n{reason}")
            photo_choices = ['static/onanism/onanizm_one.jpg']
        elif action == 'пробач_люба':
            bot.send_message(message.chat.id, f"🥺 {message.from_user.first_name} просить пробачення у своєї половинки {reply_user.first_name}\n{reason}")
            photo_choices = []
        else:
            bot.reply_to(message, "Помилка, команда неправильно прописана - перевірте її правильність. Для допомоги пропишіть /help_bot")
            return
        if photo_choices:
            photo_path = random.choice(photo_choices)
            if photo_path.endswith('.gif'):
                bot.send_animation(message.chat.id, open(photo_path, 'rb'))
            else:
                bot.send_photo(message.chat.id, open(photo_path, 'rb'))

user_choices = {}

def get_user_gender(user_id):
    gender = user_choices.get(user_id)
    if gender == 'Чоловіча':
        return 'male'
    elif gender == 'Жіноча':
        return 'female'
    else:
        return None

@bot.message_handler(commands=['стать'])
def handle_gender_choice(message):
    user_id = message.from_user.id
    if user_choices.get(user_id) is not None:
        bot.send_message(chat_id=message.chat.id, text='Ваша стать уже була обрана, для того щоб її змінити пропишіть /змінити_стать, якщо ти хочеш переглянути свою стать то пропиши /моя_стать')
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    male_button = types.InlineKeyboardButton(text='Чоловіча', callback_data='Чоловіча')
    female_button = types.InlineKeyboardButton(text='Жіноча', callback_data='Жіноча')
    markup.add(male_button, female_button)
    bot.send_message(chat_id=message.chat.id, text='Виберіть свою стать:', reply_markup=markup)
    user_choices[user_id] = None

@bot.callback_query_handler(func=lambda call: True)
def handle_gender_callback(call):
    user_id = call.from_user.id
    if user_choices.get(user_id) is not None:
        bot.send_message(chat_id=call.message.chat.id, text='Ваша стать уже була обрана, для того щоб її змінити пропишіть /змінити_стать')
        return
    user_choices[user_id] = call.data
    if call.data == 'Чоловіча':
        bot.send_message(chat_id=call.message.chat.id, text='Ваша стать обрана: Чоловіча')
    elif call.data == 'Жіноча':
        bot.send_message(chat_id=call.message.chat.id, text='Ваша стать обрана: Жіноча')

    # обробляємо команди, які використовують get_user_gender
    if call.data in ['обняти', 'поцілувати', 'вдарити', 'образити', 'чмок', 'шльоп', 'сильнийшльоп', 'кекс', 'шури-мури', 'онанізм']:
        gender = get_user_gender(user_id)
        # здійснюємо потрібну дію залежно від статі користувача


@bot.message_handler(commands=['змінити_стать'])
def handle_change_gender(message):
    user_id = message.from_user.id
    user_choices[user_id] = None
    markup = types.InlineKeyboardMarkup(row_width=2)
    male_button = types.InlineKeyboardButton(text='Чоловіча', callback_data='Чоловіча')
    female_button = types.InlineKeyboardButton(text='Жіноча', callback_data='Жіноча')
    markup.add(male_button, female_button)
    bot.send_message(chat_id=message.chat.id, text='Виберіть свою стать:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_gender_callback(call):
    user_id = call.from_user.id
    if user_choices.get(user_id) is not None:
        bot.send_message(chat_id=call.message.chat.id, text='Ваша стать уже була обрана, для того щоб її змінити пропишіть /змінити_стать')
        return
    user_choices[user_id] = call.data
    if call.data == 'Чоловіча':
        bot.send_message(chat_id=call.message.chat.id, text='Ваша стать обрана: Чоловіча')
    elif call.data == 'Жіноча':
        bot.send_message(chat_id=call.message.chat.id, text='Ваша стать обрана: Жіноча')

@bot.message_handler(commands=['моя_стать'])
def handle_gender(message):
    user_id = message.from_user.id
    gender = user_choices.get(user_id)
    if gender is not None:
        bot.send_message(chat_id=message.chat.id, text=f'Ваша стать обрана: {gender}')
    else:
        bot.send_message(chat_id=message.chat.id, text='Ви ще не обрали свою стать, для того щоб її обрати пропишіть /стать')

@bot.message_handler(
    commands=['обняти', 'поцілувати', 'вдарити', 'образити', 'чмок', 'шльоп', 'сильнийшльоп', 'кекс',
                'шури-мури', 'онанізм'])
def hug_or_kiss(message):
    gender = get_user_gender(message.from_user.id)  # виклик функції для отримання статі користувача
    if gender is None:
        bot.reply_to(message, 'Спочатку виберіть свою стать за допомогою команди /стать')
        return

@bot.message_handler(commands=['обняти'])
def hug(message):
    gender = get_user_gender(message.from_user.id)
    if gender == 'Чоловіча':
        bot.send_message(chat_id=message.chat.id, text='Ти заслуговуєш на найкраще обіймання в світі! 💪🤗')
    elif gender == 'Жіноча':
        bot.send_message(chat_id=message.chat.id, text='Дозволь мені тебе обійняти! 🤗💕')
    else:
        bot.send_message(chat_id=message.chat.id, text='Не можу зрозуміти твою стать, спочатку обери її командою /стать')


@bot.message_handler(func=lambda message: message.text.lower() in ['купити адмінку', 'купити рекламу', 'купити піар', 'піар'])
def handle_buy_command(message):
    bot.send_message(message.chat.id, 'ОУУУ чудова ідея, тоді ось тобі інформація:\n'
                                      'Молодший адмін - 20 грн\n'
                                      'Старший 50 грн\n'
                                      'Також ти можеш придбати дозвіл на опублікування реклами у цій групі, '
                                      'ось ціни:\n'
                                      'Піар 1 день - 30 грн,\n'
                                      '2 дня - 50 грн,\n'
                                      '1 тиждень - 100 грн\n'
                                      'гроші скидуй на номер карточки <code>5375 4114 2241 8942</code>, '
                                      'не переживай твої гроші підуть на добрі справи для цієї групи. \n \n'
                                      'Для того щоб купити підвищення в Ірисі плати 20 грн за кожне підвищення. \n'
                                      'Якщо ти все ж таки не хочеш купляти адмінів, тоді виконуй квести які щодня скидують'
                                      ' наші адміністратори, детальніше про квести читай тут:\n'
                                      '<a href="https://t.me/ukraine_young_chat/827665" target="_blank">https://t.me/ukraine_young_chat/827665</a>', parse_mode='html', disable_web_page_preview=True)


angel = ['ангелятко', 'ангел', 'ангелику', 'ангелочок']
insult = {'дурак', 'ідіот', 'лох', 'дибілка', 'ідіотка', 'дура', 'дибіл', 'дебіл', 'дебілка', 'дура', 'дурна', 'гей', 'лесбіянка', 'лисбіянка', 'самий уйобний бот', 'иди нахуй'}


@bot.message_handler(func=lambda message: any(word in message.text.lower() for word in insult) and any(word in message.text.lower() for word in ["ангел ти", "особа ти"]))
def handle_insult(message):
    try:
        bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=int((datetime.now() + timedelta(minutes=1)).timestamp()))
        user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        bot.send_message(message.chat.id, f"мут 1 хвилину {user_mention}", reply_to_message_id=message.message_id)
        bot.reply_to(message, "Тепер подумай над своєю поведінкою")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Мені взагаліто обідно")



        
is_shower_time = False


@bot.message_handler(commands=['вдуш'])
def handle_shower_command(message):
    global is_shower_time

    current_time = datetime.utcnow().time()

    if current_time >= time(19, 0) and current_time <= time(20, 0):
        is_shower_time = True
        bot.reply_to(message, 'Я відійшла в душ')
        time.sleep(1800)  # Почекати 30 хвилин (1800 секунд)
        bot.send_message(message.chat.id, 'Фух, все, я прийняла душ. Отже, що тепер робитимемо?')
        is_shower_time = False
    elif current_time < time(19, 0) or current_time > time(20, 0):
        try:
            bot.restrict_chat_member(
                message.chat.id, message.from_user.id,
                until_date=int((datetime.now() + timedelta(minutes=1)).timestamp())
            )
            user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
            bot.send_message(
                message.chat.id, f"Мут на 1 хвилину для {user_mention}",
                reply_to_message_id=message.message_id
            )
            bot.reply_to(
                message, "Не гарно підглядати за дівчиною в душі! Тепер подумай, як воно!"
            )
        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, "Гей, перестань, мені не приємно!")
    else:
        bot.reply_to(message, 'Ця команда доступна лише з 19:00 до 20:00')
        
        
# @bot.message_handler(commands=['вдуш'])
# def handle_shower_command(message):
#     global is_shower_time

#     current_time = datetime.utcnow().time()

#     if current_time >= time(19, 0) and current_time <= time(20, 0):
#         is_shower_time = True
#         bot.reply_to(message, 'Я відійшла в душ')
#         time.sleep(1800)  # Почекати 30 хвилин (1800 секунд)
#         bot.send_message(message.chat.id, 'Фух, все, я прийняла душ. Отже, що тепер робитимемо?')
#         is_shower_time = False
#     else:
#         try:
#             bot.restrict_chat_member(
#                 message.chat.id, message.from_user.id,
#                 until_date=int((datetime.now() + timedelta(minutes=1)).timestamp())
#             )
#             user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
#             bot.send_message(
#                 message.chat.id, f"Мут на 1 хвилину для {user_mention}",
#                 reply_to_message_id=message.message_id
#             )
#             bot.reply_to(
#                 message, "Не гарно підглядати за дівчиною в душі! Тепер подумай, як воно!"
#             )
#         except Exception as e:
#             print(e)
#             bot.send_message(message.chat.id, "Гей, перестань, мені не приємно!") - СПРОБУВАТИ!!!!

# @bot.message_handler(commands=['вдуш'])
# def handle_shower_command(message):
#     global is_shower_time

#     current_time = datetime.utcnow().time()

#     if current_time >= time(19, 0) and current_time <= time(19, 30):
#         is_shower_time = True
#         bot.reply_to(message, 'Я відійшла в душ')
#         time.sleep(1800)  # Почекати 30 хвилин (1800 секунд)
#         bot.send_message(message.chat.id, 'Фух, все я прийняла душ, отже що тепер робитимемо?')
#         is_shower_time = False
#     elif current_time < time(19, 0) and current_time > time(19, 30):
#         try:
#             bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=int((datetime.now() + timedelta(minutes=1)).timestamp()))
#             user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
#             bot.send_message(message.chat.id, f"мут 1 хвилину {user_mention}", reply_to_message_id=message.message_id)
#             bot.reply_to(message, "Не гарно підглядати за дівчиною в душі! Тепер подумай як воно!")
#         except Exception as e:
#             print(e)
#             bot.send_message(message.chat.id, "Гей, перестань, мені не приємно!")
#     else:
#         bot.reply_to(message, 'Ця команда доступна лише з 19:00 до 19:30')


# @bot.message_handler(commands=['вдуш'])
# def handle_shower_command(message):
#     global is_shower_time

#     if is_shower_time:
#         bot.reply_to(message, 'Пробач, я зараз в душі і не можу це виконати.')
#         return

#     current_time = datetime.utcnow().time()

#     if current_time >= time(19, 0) and current_time <= time(19, 30):
#         is_shower_time = True
#         bot.reply_to(message, 'Я відійшла в душ')
#         time.sleep(1800)  # Почекати 30 хвилин (1800 секунд)
#         bot.send_message(chat_id, 'Фух, все я прийняла душ, отже що тепер робитимемо?')
#         is_shower_time = False
#     elif current_time < time(19, 0) and current_time > time(19, 30):
#         try:
#             bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=int((datetime.now() + timedelta(minutes=1)).timestamp()))
#             user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
#             bot.send_message(message.chat.id, f"мут 1 хвилину {user_mention}", reply_to_message_id=message.message_id)
#             bot.reply_to(message, "Не гарно підглядати за дівчиною в душі! Тепер подумай як воно!")
#         except Exception as e:
#             print(e)
#             bot.send_message(message.chat.id, "Гей, перестань, мені не приємно!")
#     else:
#         bot.reply_to(message, 'Ця команда доступна лише з 19:00 до 19:30')

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
#         'не': 'ні',
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
#         'мне': 'мені',
#         'ему': 'йому',
#         # Додайте сюди інші слова та їх переклади
#     }
#     return translation_dict.get(word, word)

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


# @bot.message_handler(func=lambda message: True)
# def handle_all_commands(message):
#     communication.handle_commands(bot, message)
    
# @bot.message_handler(func=lambda message: True)
# def handle_all_commands(message):
#     communication.handle_commands(bot, message);
#     translate.handle_message(bot, message);

# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     communication.handle_commands(bot, message)
#     translate.handle_message(bot, message)

@bot.message_handler(func=lambda message: True)
def handle_all_commands(message):
#     translate.handle_message(bot, message)
#     translate.handle_message(message)
    communication.handle_commands(bot, message)
#     translate.handle_message(bot, message)

bot.polling(none_stop=True)
