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
from datetime import datetime, timedelta, time
#import json
import re
#import yagmail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(config.TOKEN)


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
                                      "піар або адмінку, просто пропиши: купити піар, або купити адмінку</b>", parse_mode='html', disable_web_page_preview=True)
    bot.send_photo(message.chat.id, open('static/01.jpg', 'rb'))


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
        elif action == 'вдарити':
            bot.send_message(message.chat.id, f" 🤜🤕 {message.from_user.first_name} вдарив(-ла) {reply_user.first_name}\n{reason}")
            photo_choices = ['static/bully/bully_one.gif', 'static/bully/bully_two.gif', 'static/bully/bully_three.gif',
                             'static/bully/bully_four.gif', 'static/bully/bully_five.gif', 'static/bully/bully_six.gif',
                             'static/bully/bully_seven.gif', 'static/bully/bully_eight.gif', 'static/bully/bully_nine.gif'
                             'static/bully/bully_ten.gif']
        elif action == 'образити':
            bot.send_message(message.chat.id, f"😒 {message.from_user.first_name} образив(-ла) {reply_user.first_name}\nПричина: {reason}")
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
            photo_choices = ['static/se/se_one.gif', 'static/se/se_two.gif', 'static/se/se_three.webp']
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
                                      'не переживай твої гроші підуть на добрі справи для цієї групи \n \n'
                                      'Якщо ти все ж таки не хочеш купляти адмінів, тоді виконуй квести які щодня скидують'
                                      'наші адміністратори, детальніше про квести читай тут:\n'
                                      '<a href="https://t.me/ukraine_young_chat/827665" target="_blank">https://t.me/ukraine_young_chat/827665</a>', parse_mode='html', disable_web_page_preview=True)


angel = ['ангелятко', 'ангел', 'ангелику', 'ангелочок']
insult = {'дурак', 'ідіот', 'лох', 'дибілка', 'ідіотка', 'дура', 'дибіл', 'дебіл', 'дебілка', 'дура', 'дурна', 'гей', 'лесбіянка', 'лисбіянка', 'самий уйобний бот', 'иди нахуй'}
is_shower_time = False


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





@bot.message_handler(commands=['вдуш'])
def handle_shower_command(message):
    global is_shower_time

    if is_shower_time:
        bot.reply_to(message, 'Пробач, я зараз в душі і не можу це виконати.')
        return

    current_time = datetime.utcnow().time()

    if current_time < time(13, 0) or current_time > time(19, 30):
        bot.reply_to(message, 'Ні, я ще не йду купатися, тому розслабся.')
        return

    if current_time >= time(13, 0) and current_time <= time(19, 30):
        is_shower_time = True
        bot.reply_to(message, 'Я відійшла в душ')
        time.sleep(1800)  # Почекати 30 хвилин (1800 секунд)
        bot.send_message(chat_id, 'Фух, все я прийняла душ, отже що тепер робитимемо?')
        is_shower_time = False
    elif current_time >= time(19, 0) and current_time <= time(19, 45):
        bot.reply_to(message, 'Гей, перестань!')
    else:
        bot.reply_to(message, 'Сталася помилка')






@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    answered_question = False
    for keyword in angel:
        if text == f"{keyword} представся" or text == f"{keyword} представлення" or text == f"{keyword} хто ти" or text == f"{keyword} команди" or text == f"{keyword} що вмієш":
            bot.send_message(message.chat.id, 'Привіт, я ангел, я можу спілкуватися з вами або ж виконувати команди такі як:'
                                              '\n\n<b>/від вдарити</b>, \n<b>/від обняти</b>, \n<b>/від поцілувати</b> \n<b>/від образити</b>'
                                              '\n<b>/від чмок</b>\n<b>/від шльоп</b>\n<b>/від сильнийшльоп</b>\n<b>/від кекс або ж /від секс</b>\n<b>/від онанізм</b>'
                                              '\n<b>/від засос</b>\n<b>/стать</b>'
                                          '\n<b>Відповідати на запитання на скільки хтось розумний чи дурний</b>\n<b>Відповідати на запитання так чи ні '
                                              '(В кінці обовязково напиши ?, для прикладу: ангел таке можливе?)</b>\n\nТакож я маю звичайні команди як:'
                                              '\n\n<b>показати ніжки</b>\n\n<b>А також я можу надавати інформацію про те як купити піар або адмінку, просто '
                                              'пропиши: купити піар, або купити адмінку</b>\n\nА і ще одне, з 19:00 до 19:30 я іду в душ, кожного дня, тому хлопчики - '
                                              'не заглядати, а то покараю\n'
                                          '\nІ хлопчики, будь ласка, будьте зі мною лагідні а також із своїми дівчатками'.format(message.from_user, bot.get_me()),
            parse_mode='html')
            photo_choices = ['static/01.jpg']
            photo = open(random.choice(photo_choices), 'rb')
            bot.send_photo(message.chat.id, photo)
        elif text in [f"{keyword} привіт", f"{keyword} привет", f"{keyword} хай", f"{keyword} здоров"]:
            bot.send_message(message.chat.id, 'Привіт')
        elif text in [f"{keyword} як ти", f"{keyword} як справи", f"{keyword} ти як", f"{keyword} як ти?", f"{keyword}, ти як", f"{keyword}, ти як?"]:
            bot.send_message(message.chat.id, 'Усе гаразд, а ти як?')
        elif text == f"{keyword} дякую" or text == f"дякую {keyword}":
            bot.send_message(message.chat.id, 'Завжди прошу, моє кошенятко 😘')
        #elif text == f"{keyword} що ти вмієш?" or text == f"{keyword} що ти можеш?":
        #    bot.send_message(message.chat.id, 'Я можу відповісти на твої запитання, показати картинки, розповісти анекдоти і багато іншого!')
        #elif text == f"{keyword} допоможи" or text == f"{keyword} допоможи мені":
        #    bot.send_message(message.chat.id, 'Звісно, що допоможу! Що тобі потрібно?')
        #elif text == f"{keyword} дай пораду" or text == f"{keyword} порадь":
        #    bot.send_message(message.chat.id, 'Моя порада: будь завжди веселим і позитивним!')
        elif text == f"{keyword} до побачення" or text == f"{keyword} бувай":
            bot.send_message(message.chat.id, 'До зустрічі! Бувай ❤')
        elif text == f"{keyword} на добраніч" or text == f"{keyword} спокійної ночі" or text == f"{keyword} надобраніч":
            bot.send_message(message.chat.id, 'На добраніч моє кошеня 😘❤')
        elif text == f"{keyword} вірш" or text == f"{keyword} поезія":
            bot.send_message(message.chat.id, 'А ось і мій вірш:\nТи мій ангел, що з неба злетів,\nЩоб мені допомогти в біді,\nЗавжди поруч, коли я сам,\nТи мій ангел, мій друг і мій брат.')
#=================================================================================================================
    #elif message.reply_to_message is not None and message.text.lower() == 'ангел скажи наскільки він розумний':
    #    bot.send_message(message.chat.id, f"Небеса кажуть що він розумний на {random.randint(0, 100)}%")
    #elif message.reply_to_message is not None and message.text.lower() in ['ангел скажи наскільки вона розумна', 'ангел на скільки вона розумна']:
    #    bot.send_message(message.chat.id, f"Небеса кажуть що вона розумна на {random.randint(0, 100)}%")
    #elif message.reply_to_message is not None and message.text.lower() == 'ангел скажи наскільки він дурний?':
    #    bot.send_message(message.chat.id, f"Небеса кажуть що він дурний на {random.randint(0, 100)}%")
    #elif message.reply_to_message is not None and message.text.lower() == 'ангел скажи наскільки вона дурна?':
    #    bot.send_message(message.chat.id, f"Небеса кажуть що вона дурна на {random.randint(0, 100)}%")
#======================================================================================================================
        elif text.startswith(f"{keyword} ") and '?' in text:
            bot.send_message(message.chat.id, random.choice(['Так', 'Ні']))
        elif text.startswith(f"{keyword}") and 'хто' in text:
            bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто']))
        elif re.search(r"\bангел\b.*\bскільки\b.*\bразів\b.*\bтиждень\b.*[.?!]", text, re.IGNORECASE) and not answered_question:
            bot.send_message(message.chat.id, 'Десь ' + str(random.randint(1, 10)))
            answered_question = True



        elif text == f"{keyword} ти умнічка" or text == f"{keyword} ти молодець" or text == f"{keyword} розумниця" or text == f"{keyword} умнічка" or text == f"{keyword} молодець":
            bot.send_message(message.chat.id, 'Дякую кошеннятко моє 😍 😘, мені приємно це знати')
        elif text == f"{keyword}" or text == f"{keyword} ти тут" or text == f"{keyword} ти де":
            bot.send_message(message.chat.id, 'Так я тут, пробач що затримала')
        elif text == f"показати ніжки" or text == f"ніжки" or text == f"{keyword} покажи ніжки" or text == f"{keyword} покажи свої ніжки" or text == f"покажи ніжки":
            bot.send_message(message.chat.id, f"🤗 {message.from_user.first_name} вирішив(-ла) подивитися на ніжки")
            photo_choices = ['static/legs/legs_(1).jpg', 'static/legs/legs_(2).jpg', 'static/legs/legs_(3).jpg',
                     'static/legs/legs_(4).jpg', 'static/legs/legs_(5).jpg', 'static/legs/legs_(6).jpg',
                     'static/legs/legs_(7).jpg', 'static/legs/legs_(8).jpg', 'static/legs/legs_(9).jpg',
                     'static/legs/legs_(10).jpg', 'static/legs/legs_(11).jpg', 'static/legs/legs_(12).jpg',
                     'static/legs/legs_(13).jpg', 'static/legs/legs_(14).jpg',
                     'static/legs/legs_(16).jpg', 'static/legs/legs_(17).jpg', 'static/legs/legs_(18).jpg',
                     'static/legs/legs_(19).jpg', 'static/legs/legs_(20).jpg', 'static/legs/legs_(21).jpg',
                     'static/legs/legs_(22).jpg', 'static/legs/legs_(23).jpg', 'static/legs/legs_(24).jpg',
                     'static/legs/legs_(25).jpg', 'static/legs/legs_(26).jpg', 'static/legs/legs_(27).jpg',
                     'static/legs/legs_(28).jpg', 'static/legs/legs_(29).jpg', 'static/legs/legs_(30).jpg',
                     'static/legs/legs_(31).jpg', 'static/legs/legs_(32).jpg']
            photo_path = random.choice(photo_choices)
            with open(photo_path, 'rb') as photo_file:
                bot.send_photo(message.chat.id, photo_file)

bot.polling(none_stop=True)
