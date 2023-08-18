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
from pyaspeller import YandexSpeller
import math
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(config.TOKEN)

# @bot.message_handler(commands=['написати_власнику'])
# def send_email(message):
#     bot.send_message(message.chat.id, "Будь ласка введіть ваше повідомлення:")
#     bot.register_next_step_handler(message, send_email_message)

# def send_email_message(message):
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login('romanhnatiak@gmail.com', config.email_password)
#         to_email = 'romanhnatiak@gmail.com'
#         subject = 'Повідомлення від користувача'
#         email_text = f"Від: {message.from_user.username}\nСмс: {message.text}"
#         message = 'Subject: {}\n\n{}'.format(subject, email_text)
#         server.sendmail('angel31@gmail.com', to_email, message)
#         server.quit()
#         bot.send_message(message.chat.id, "Чудово, ваш лист надіслано!")
#     except:
#         bot.send_message(message.chat.id, "На жаль щось пішло не так, повторіть операцію пізніше.")



pending_friendships = {}
friendships = []







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
# def end_game(message):
#     user_id = message.from_user.id

#     if user_id in game_numbers:
#         del game_numbers[user_id]
#         bot.send_message(chat_id=message.chat.id, text='Гра була закінчена.')
#     else:
#         bot.send_message(chat_id=message.chat.id, text='Ви не брали участі в жодній грі.')





# ukrainian_alphabet = ['а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о',
#                       'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ю', 'я']

# excluded_words = ['сука', 'стриптиз', 'секс', 'апарат', 'апаратура', 'аромат', 'кріт', 'абориген', 'аплодисменти', 'апокаліпсис', 'аркада', 'аркади', 
#                   'кірка', 'ящірка', 'турція', 'тінь', 'аксесуар', 'анакондра', 'акорд', 'амілія', 'ярлик', 'шашлик', 'ананас', 'ренген', 'рись', 'павлін', 
#                   'романтичний', 'романтика', 'акордеон']
# special_ukrainian_words = {
#     'окунь': 'н',
#     'еге': 'г',
#     'ніготь': 'т',
#     'кіготь': 'т',
#     'ячмінь': 'н',
#     'лебідь': 'д',
#     'танець': 'ц',
#     'тернопіль': 'л',
#     'аркади': 'д',
#     'тінь': 'н',
#     'алкоголь': 'л',
#     'контроль': 'л',
#     'поршень': 'н',
#     'король': 'л',
# }

# not_correct_ukrainian_words = ['продек', 'пкопр', 'пкойцв', 'цушгк', 'нейросеть', 'енор']

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


user_choices = {}

gender = ""


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
        elif action in ('вдарити', 'удар', 'ударити', 'гримнути'):
            bot.send_message(message.chat.id, f" 🤜🤕 {message.from_user.first_name} вдарив(-ла) {reply_user.first_name}\n{reason}")
            photo_choices = ['static/bully/bully_one.gif', 'static/bully/bully_two.gif', 'static/bully/bully_three.gif', 'static/bully/bully_four.gif', 'static/bully/bully_five.gif', 'static/bully/bully_six.gif', 'static/bully/bully_seven.gif', 'static/bully/bully_eight.gif', 'static/bully/bully_nine.gif', 'static/bully/bully_ten.gif']
        elif action == 'образити':
            bot.send_message(message.chat.id, f"😒 {message.from_user.first_name} образив(-ла) {reply_user.first_name}\n{reason}")
            photo_choices = []
        elif action in ['потиснути руку', 'пожати руку', 'пожати']:
            bot.send_message(message.chat.id, f"🤗 {message.from_user.first_name} пожав руку {reply_user.first_name}\n{reason}")
            photo_choices = []
        elif action == 'чмок':
            bot.send_message(message.chat.id, f"🤗 {message.from_user.first_name} чмокнув(-ла) {reply_user.first_name}\n{reason}")
            photo_choices = ['static/kisses/kiss_one.jpg', 'static/kisses/kiss_two.jpg', 'static/kisses/kiss_three.jpg', 'static/kisses/kiss_four.jpg', 'static/kisses/kiss_one.jpg', 'static/kisses/kiss_five.jpg', 'static/kisses/kiss_six.jpg', 'static/kisses/kiss_seven.jpg']
        elif action == 'шльоп':
            bot.send_message(message.chat.id, f"🤗 {message.from_user.first_name} шльопнув(-ла) {reply_user.first_name}\n{reason}")
            photo_choices = ['static/slaps/slap_one.gif', 'static/slaps/slap_two.gif', 'static/slaps/slap_three.gif', 'static/slaps/slap_four.gif']
        elif action == 'сильнийшльоп':
            bot.send_message(message.chat.id, f"🤗 {message.from_user.first_name} зі всієї дурі шльопнув(-ла) {reply_user.first_name}\n{reason}")
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
        elif action in ('пробач', 'вибач', 'вибач мені люба', 'пробач кошеня', 'вибач кохана', 'вибач мені кохана', 'вибач мені кошеня', 'пробач мені люба' , 'пробач мені люба я не хотів'):
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
        


player_scores = {}  # Словник для збереження балів гравців
QUEST_THRESHOLD = 1000  # Поріг для виконання квесту
MIN_WORDS_THRESHOLD = 3

def translate_russian_to_ukrainian(word):
    translation_dict = {
        'ё': 'їо',
        'ы': 'и',
        'эту': 'цю',
# А
    
# Б
        'бистро': 'швидко',
        'больше': 'більше',
        'боюсь': 'боюся',
        'бес': 'біс',
        'бесит': 'бісить',
        
# В
        'вопрос': 'питання/запитання',
        'вопросы': 'питання/запитання',
        'взрывают': 'взривають/підривають',
        'випитой': 'випитої',
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
        'им': 'їм',
        'игру': '(і)гру',
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
        'летят': 'летять',
        'литров': 'літрів',
        
# М
        'мать': 'мати',
        'меня': 'мене',
        'мы': 'ми',
        'мой': 'мій',
        'мне': 'мені',
        'молчи': 'мовчи',
        'можно': 'можна',
        
        
# Н
#       'не': 'ні', ВИКЛЮЧЕННЯ
        'наконец-то': 'нарешті/накінець-то',
        'надо': 'потрібно',
        'нечего': 'нічого',
        'немного': 'трохи/трішки',
        'немножко': 'трішки/трошки',
        'нет': 'ні/немає',
        'ничего': 'нічого',
        'но': 'але',
        
# О
        'от': 'від/з/ось',
        'опрос': 'питання/запитання',
        'опросы': 'питання/запитання',
        
# П
        'попробуем': 'спробуємо',
        'понятно': 'зрозуміло',
        'похож': 'похожий/схожий/подібний',
        'почему': 'чому',
        'почти': 'майже',
        'писать': 'писати',
        'привет': 'привіт',
        'привык': 'привик/звик',
        'птичка': 'пташка',
        'птички': 'пташки',
        

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
        'твоёй': 'твоїй',
        'ты': 'ти',
        'тебя': 'тебе',
        'только': 'тільки/лише',
        'тяжело': 'важко/тяжко',

# У
#         'уже': 'вже', ВИНЯТОК
        'уверен': 'впевнений',
        'уверена': 'впевнена',
        'увидеть': 'побачити',

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
        'чуток': 'трохи',

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
    sorted_players = sorted(player_scores.items(), key=lambda x: x[1]['score'], reverse=True)
    reply = "Рейтинг гравців:\n\n"
    for i, (player_id, player) in enumerate(sorted_players, start=1):
        player_name = bot.get_chat_member(message.chat.id, player_id).user.first_name
        reply += f"{i}. {player_name} - {player['score']} {player['quests']} виконаних квестів\n"
    reply += "\nЯкщо ти новенький, тоді пропиши /українські_бали_правила і прочитай які умови і як в це грати"
    bot.send_message(message.chat.id, reply)

# @bot.message_handler(commands=['українські_бали'])
# def display_scores(message):
#     sorted_players = sorted(player_scores.items(), key=lambda x: x[1]['score'], reverse=True)
#     total_players = len(sorted_players)
#     page_size = 10  # Number of players to display per page
#     total_pages = math.ceil(total_players / page_size)

#     page = 1  # Initial page number
#     display_players = sorted_players[(page - 1) * page_size:page * page_size]

#     reply = get_scoreboard_reply(display_players, page, total_pages, message)
#     bot.send_message(message.chat.id, reply)

# def get_scoreboard_reply(players, current_page, total_pages, message, sorted_players):
#     reply = "Рейтинг гравців:\n\n"
#     for i, (player_id, player) in enumerate(sorted_players, start=1):
#         player_name = bot.get_chat_member(message.chat.id, player_id).user.first_name
#         reply += f"{i}. {player_name} - {player['score']} {player['quests']} виконаних квестів\n"
#     reply += "\nЯкщо ти новенький, тоді пропиши /українські_бали_правила і прочитай які умови і як в це грати"

#     reply += f"\nСторінка {current_page} з {total_pages}"

#     if total_pages > 1:
#         keyboard = []
#         if current_page > 1:
#             prev_button = InlineKeyboardButton("<< Попередня", callback_data=f"prev_page:{current_page}")
#             keyboard.append(prev_button)
#         if current_page < total_pages:
#             next_button = InlineKeyboardButton("Наступна >>", callback_data=f"next_page:{current_page}")
#             keyboard.append(next_button)
#         reply_markup = InlineKeyboardMarkup([keyboard])
#         reply += "\n\nНатисни кнопку, щоб переглянути інших учасників."

#     return reply

# @bot.message_handler(commands=['українські_бали_правила'])
# def display_rules(message):
#     rules = "Правила гри:\n"
#     rules += "1. Бали нараховуються за кожне правильне слово українською мовою.\n"
#     rules += "2. За кожне слово, яке НЕ існує в українській мові, гравцю знімається 1 бал.\n"
#     rules += "3. Якщо слово містить букви 'ё' або 'ы', гравцю також знімається 1 бал.\n"
#     rules += "4. Після набору 1000 балів гравець отримує +1 виконаний квест, після чого його бали обнуляються автоматично.\n"
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

@bot.message_handler(func=lambda message: True)
def handle_all_commands(message):
    communication.handle_commands(bot, message)

# @bot.message_handler(func=lambda message: True)
# def handle_all_messages(message):
#     translate.handle_message(bot, message)

bot.polling(none_stop=True)
