# -*- coding: utf-8 -*-

import types
import telebot
import config
import random
import logging
import time
from telebot import TeleBot, types
from datetime import datetime, timedelta, time
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import speakwithbot.communication as communication
from langdetect import detect
from pyaspeller import YandexSpeller
import math
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(config.TOKEN)

pending_friendships = {}
friendships = []

player_scores = {}
QUEST_THRESHOLD = 1000
MIN_WORDS_THRESHOLD = 3
game_numbers = {}

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

@bot.message_handler(commands=['закінчити_гру_в_цифри'])
def end_game(message):
    user_id = message.from_user.id

    if user_id in game_numbers:
        del game_numbers[user_id]
        bot.send_message(chat_id=message.chat.id, text='Гра була закінчена.')
    else:
        bot.send_message(chat_id=message.chat.id, text='Ви не брали участі в жодній грі.')

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
        elif action in ('пробач', 'вибач'):
            bot.send_message(message.chat.id, f"🥺 {message.from_user.first_name} просить пробачення у своєї половинки {reply_user.first_name}")
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

    if call.data in ['обняти', 'поцілувати', 'вдарити', 'образити', 'чмок', 'шльоп', 'сильнийшльоп', 'кекс', 'шури-мури', 'онанізм']:
        gender = get_user_gender(user_id)


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
insult = {'дурак', 'ідіот', 'лох', 'дибілка', 'ідіотка', 'дура', 'сядешь мені на хуй', 'від сосешь мені', 'сядь мені на хуй', 'пошла на хуй', 'ти сосешь', 'станеш раком', 'стань раком', 'дибіл', 'дебіл', 'дебілка', 'дура', 'дурна', 'гей', 'лесбіянка', 'лисбіянка', 'самий уйобний бот', 'иди нахуй', 'будеш сосать члена', 'будеш сосать', 'сосать', 'соси', 'соси член'}


@bot.message_handler(func=lambda message: any(word in message.text.lower() for word in insult) and any(word in message.text.lower() for word in ["ангел ти", "особа ти", "ангел", 'ангел ', 'Ангел ', 'Ангел', 'Ангел ти ']))
def handle_insult(message):
    try:
        bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=int((datetime.now() + timedelta(minutes=1)).timestamp()))
        user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        bot.send_message(message.chat.id, f"мут 1 хвилину {user_mention}", reply_to_message_id=message.message_id)
        bot.reply_to(message, "Тепер подумай над своєю поведінкою")
    except Exception as e:
        bot.send_message(message.chat.id, "Мені взагаліто обідно")



        
is_shower_time = False


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
#     elif current_time < time(19, 0) or current_time > time(20, 0):
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
#             bot.send_message(message.chat.id, "Гей, перестань, мені не приємно!")
#     else:
#         bot.reply_to(message, 'Ця команда доступна лише з 19:00 до 20:00')


@bot.message_handler(commands=['вдуш'])
def handle_shower_command(message):
    global is_shower_time

    current_time = datetime.utcnow().time()

    # Check if it's shower time (from 19:00 to 20:00)
    if current_time >= time(19, 0) and current_time <= time(20, 0):
        is_shower_time = True
        bot.reply_to(message, 'Я відійшла в душ')
        time.sleep(1800)  # Wait for 30 minutes (1800 seconds)
        bot.send_message(message.chat.id, 'Фух, все, я прийняла душ. Отже, що тепер робитимемо?')
        is_shower_time = False
    else:
        # If it's not shower time, inform the user about the restricted command
        bot.reply_to(message, 'Ця команда доступна лише з 19:00 до 20:00')

        # If someone tries to use the command outside shower time, restrict them
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
            bot.send_message(message.chat.id, "Гей, перестань, мені не приємно!")


def translate_russian_to_ukrainian(word):
    translation_dict = {
        'ё': 'їо',
        'ы': 'и',
        'эту': 'цю',
        'это': 'це',
        'этот': 'цей',
        'этого': 'цього',
# А
        'акуратно': 'окуратно',
        'акуратна': 'окуратно',
        'ахуел': 'офігів/здурів',
# Б
        'бистро': 'швидко',
        'бизнес': 'бізнес',
        'болтать': 'розмовляти/говорити/бовтати',
        'больше': 'більше',
        'большие': 'великі',
        'больницу': 'лікарню',
        'больница': 'лікарня',
        'боюсь': 'боюся',
        'бес': 'біс',
        'бесит': 'бісить',
        'будет': 'буде',
        'будем': 'будемо',
        'беспокоит': 'турбує/хвилює',
        'бухать': 'бухати/пити',
        'беспокоить': 'турбує/хвилює',
        'было': 'було',
        'будешь': 'будеш',
        'блять': 'блінчик',
# В
        'вашем': 'вашу',
        'вопрос': 'питання/запитання',
        'вопросы': 'питання/запитання',
        'взрывают': 'взривають/підривають',
        'випитой': 'випитої',
        'всем': 'всім',
        'вылезло': 'вилізло',
        'видеш': 'бачиш',
        'врага': 'ворога',
        'враг': 'ворог',
        'всего': 'всього',
# Г
        'где': 'де',
        'говоришь': 'говориш/кажеш/розмовляєш/спілкуєшся',
        'города': 'міста',
        'гони': 'віддавай/давай',
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
        'доверяю': 'довіряю',
        'доброе': 'Доброго',
        'деньги': 'гроші',
        'должно': 'повинно/має',
        'делаешь': 'робиш',
        'дела': 'справи',
        'делать': 'робити',
        'дом': 'дім/будинок',
        'думаешь': 'думаєш',
# Е
        'ему': 'йому',
        'её': 'її',
        'ей': 'їй',
        'его': 'його',
        'если': 'якщо',
        'есть': 'є',
        'ещё': 'ще',
        'ето': 'це',
        'еж': 'їжак',
        'ем': 'їм',
        'ежа': 'їжака',
        'еште': 'їжте',
        'еще': 'ще',
# Є

# Ж
        'же': 'ж',
        'жёстко': 'жорстоко',
        'жосткие': 'жорстокі',
        'жду': 'чекаю',
        'женщин': 'жінок',
# З
        'заболеть': 'захворіти',
        'заболел': 'захворів',
        'заболела': 'захворіла',
        'закрой': 'закрий',
        'зонтик': 'парасоля',
        'зонтик': 'парасоля',
        'здарова': 'здоров',
        'заходить': 'заходити',
        'значит': 'значить/це означає',
        'замутил': 'замутив',
# И
        'и': 'і',
        'или': 'або',
        'итак': 'і так',
        'им': 'їм',
        'игра': 'гра/ігра',
        'игру': '(і)гру',
        'иди': 'йди/іди',
        'изнасиловал': 'зґвалтував',
        'изнасиловала': 'зґвалтувала',
        'изнасиловала': 'зґвалтувала',
        'информация': 'інформація',
        'именно': 'саме',
        'имба': 'топ',
        'ичо': 'і що',
# І
        'ічо': 'і що',
        'і чо': 'і що',
# Ї

# Й

# К
        'к': 'до',
        'как': 'як',
        'канеш': 'звісно',
        'каждый': 'кожен',
        'кароче': '(одним) словом',
        'канешно': 'звісно',
        'конечно': 'звісно',
        'конешно': 'звісно',
        'канешно': 'звісно',
        'когда': 'коли',
        'красивый': 'красивий',
        'какого': 'якого',
        'какова': 'якого',
        'кто': 'хто',
        'купить': 'купити',
        'кришы': 'даху',
# Л
        'ладно': 'гаразд/окей',
        'летят': 'летять',
        'литров': 'літрів',
        'лошадиных': 'конячих',
        'любые': 'любі',
        'лета': 'літа',
        'лето': 'літо',
        'лиш': 'лише',
# М
        'машины': 'машини',
        'матов': 'матів/матюків',
        'мать': 'мати',
        'меня': 'мене',
        'мы': 'ми',
        'мой': 'мій',
        'мной': 'мною',
        'мне': 'мені',
        'молчи': 'мовчи',
        'молчат': 'мовчать',
        'молчал': 'мовчав',
        'можно': 'можна',
        'морозит': 'морозить',
        'мрази': 'зарази',
        'минет': 'мінет',
        'месячные': 'місячні',
        'миленькая': 'мила',
        'мышки': 'мишки',
# Н
#       'не': 'ні', ВИКЛЮЧЕННЯ
        'надо': 'потрібно',
        'найти': 'знайти',
        'настроение': 'ністрій',
        'наконец-то': 'нарешті/накінець-то',
        'надо': 'потрібно',
        'нечего': 'нічого',
        'немного': 'трохи/трішки',
        'немножко': 'трішки/трошки',
        'нет': 'ні/немає',
        'ничего': 'нічого',
        'но': 'але',
        'ночь': 'ніч',
        'надоело': 'набридло/надоїло',
        'ножку': 'ніжку',
# О
        'о': 'про',
        'общения': 'спілкування/комунікації',
        'общаються': 'розмовляють/спілкуються',
        'он': 'він',
        'она': 'вона',
        'от': 'від/з/ось',
        'опрос': 'питання/запитання',
        'опросы': 'питання/запитання',
        'отрежим': 'відріжем(-о)',
        'одиночка': 'сам(-а)',
        'опять': 'знову',
        'обнять': 'обняти/обійняти',
        'отлизал': 'відлизав',
# П
        'падает': 'падає',
        'патриоткой': 'патріоткою',
        'патриот': 'патріот',
        'патриотом': 'патріотом',
        'пасть': 'писок',
        'парнем': 'хлопцем',
        'попробуем': 'спробуємо',
        'познакомлюсь': 'познайомлюсь',
        'понятно': 'зрозуміло',
        'понял': 'зрозумів',
        'похож': 'похожий/схожий/подібний',
        'почему': 'чому',
        'посадят': 'посадять',
        'поставил': 'поставив',
        'после': 'після',
        'поцеловать': 'поцілувати',
        'почти': 'майже',
        'под': 'під',
        'пошло': 'пішло',
        'пошел': 'пішов',
        'писать': 'писати',
        'пишите': 'пишіть',
        'привет': 'привіт',
        'приветик': 'привітик',
        'привык': 'привик/звик',
        'продать': 'продати',
        'птичка': 'пташка',
        'птички': 'пташки',
        'песня': 'пісня',
        'пока': 'бувай(-те)/до зустрічі',
        'поможет': 'допоможе',
        'поднять': 'підняти',
        'проблемы': 'проблеми',
        'пятницу': 'п\'ятницю',
        'понедельник': 'понеділок',
        'помидоров': 'помідорів',
        'последние': 'останні',
        'понимаю': 'розумію',
        'правильная': 'правильна',
        'проверку': 'перевірку',
        'проверка': 'перевірка',
        'перережу': 'переріжу',
        'перерезал': 'перерізав',
        'перерезала': 'перерізала',
        'песню': 'пісню',
        'последний': 'останній',
        'подмишки': 'пахви',
        'подмышки': 'пахви',
# Р
        'разгон': 'розгін',
        'работает': 'працює',
        'ребят': 'друзі',
# С
        'c': 'з',
        'cо': 'зі',
        'свой': 'свій',
        'свете': 'світі',
        'сейчас': 'зараз / на даний момент',
        'сладкие': 'солодкі',
        'сладкая': 'солоденька/солодка',
        'сладка': 'солодко',
        'сложный': 'важкий',
        'сложна': 'важка/важко',
        'спасиба': 'Дякую',
        'спасибо': 'дякую',
        'сделал': 'зробив',
        'сделайте': 'зробіть',
        'сделала': 'зробила',
        'скучно': 'нудно',
        'скорость': 'швидкість',
        'снова': 'знову',
        'серовно': 'все одно',
        'слиш': 'слухай',
        'сказать': 'сказати',
        'сможешь': 'зможеш',
        'создав': 'створив',
        'сука': 'зараза',
# Т
        'такое': 'таке',
#       'тебе': 'тобі', ВИКЛЮЧЕННЯ
        'темы': 'теми',
        'твоёй': 'твоїй',
        'ты': 'ти',
        'тебя': 'тебе',
        'только': 'тільки/лише',
        'тяжело': 'важко/тяжко',
        'том': 'цьому',
        'тракторе': 'тракторі',
# У
#         'уже': 'вже', ВИНЯТОК
        'уверен': 'впевнений',
        'уверена': 'впевнена',
        'увидеть': 'побачити',
        'утро': 'ранок',
        'умею': 'вмію',
        'убери': 'забери/прибери',
        'убере': 'забере/прибере',
# Ф
        'франсузком': 'французькій',
# Х
        'хотел': 'хотів',
        'хотела': 'хотіла',
        'хорошо': 'добре',
        'харасьо': 'гаразд/окі',
        'хочешь': 'хочеш',
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
        'честно': 'чесно',
        'чтобы': 'щоб',
        'четверг': 'четвер',
# Ш
        'шо': 'що',
        'што': 'що',
        'шуткую': 'жартую',
# Щ
        'щяс': 'зараз',

# Ь

# Ю

# Я
    }
    return translation_dict.get(word, word)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    player_id = message.from_user.id
    text = message.text.lower()
    words = re.findall(r'\b\w+\b', text)

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

    communication.handle_commands(bot, message)

bot.polling(none_stop=True)
