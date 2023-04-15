# -*- coding: utf-8 -*-

import types
import telebot
import config
import random
import logging
import datetime
#from telebot import types
#import sqlite3
#from sqlite3 import Error
from telebot import TeleBot, types
#from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#from telegram.ext import CallbackContext
from datetime import datetime, time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['help_bot'])
def greeting(message):
    bot.send_message(message.chat.id, "У мене доступні такі команди як:\n<b>/від вдарити</b>, \n<b>/від обняти</b>, "
                                      "\n<b>/від поцілувати</b> \n<b>/від образити</b>\n<b>/від чмок</b>\n<b>/від шльоп</b>"
                                      "\n<b>/від сильнийшльоп</b>\n<b>/від кекс або ж /від секс</b>\n<b>/від онанізм</b>"
                                      "\n<b>/від засос</b>\n<b>/стать</b>\n<b>Відповідати на запитання на скільки хтось розумний чи дурний</b>"
                                      "\n<b>Відповідати на запитання так чи ні (В кінці обовязково напиши ?, для прикладу: ангел таке можливе?)</b>"
                                      "\nТакож я маю звичайні команди як:\n<b>показати ніжки</b>\n<b>А також я можу надавати інформацію про те як купити "
                                      "піар або адмінку, просто пропиши: купити піар, або купити адмінку</b>", parse_mode='html', disable_web_page_preview=True)














user_choices = {}

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
            bot.send_message(message.chat.id, f" 🤜🤕 {message.from_user.first_name} вдарив(-ла) {reply_user.first_name}\nПричина: {reason}")
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
            bot.send_message(message.chat.id, f"🥵 {message.from_user.first_name} зайнявся самозадоволенням\n{reason}")
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
    male_button = types.InlineKeyboardButton(text='Чоловіча', callback_data='male')
    female_button = types.InlineKeyboardButton(text='Жіноча', callback_data='female')
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
    if call.data == 'male':
        bot.send_message(chat_id=call.message.chat.id, text='Ваша стать обрана: Чоловіча')
    elif call.data == 'female':
        bot.send_message(chat_id=call.message.chat.id, text='Ваша стать обрана: Жіноча')

@bot.message_handler(commands=['обняти'])
def hug(update, context):
    user_id = update.message.from_user.id
    gender = get_user_gender(user_id)
    if gender == 'male':
        update.message.reply_text('Ти обіймаєшся з хлопцем. ❤️')
    elif gender == 'female':
        update.message.reply_text('Ти обіймаєшся з дівчиною. ❤️')
    else:
        update.message.reply_text('Ти обіймаєшся зі створінням. ❤️')
















proposals = {}

@bot.message_handler(func=lambda message: message.text.startswith('/одружитися'))
def handle_all_messages(message):
    chat_id = message.chat.id
    reply_user = message.reply_to_message.from_user if message.reply_to_message else None
    text = message.text

    if text == '/start_Angel32':
        bot.send_message(chat_id,
                        'Привіт! Я бот для одруження. Я можу допомогти вам одружитися, просто напишіть /одружитися, щоб запропонувати руку і серце комусь.')

    elif text == '/одружитися' and reply_user:
        proposals[reply_user.id] = {
            'from_user_id': message.from_user.id,
            'chat_id': chat_id
        }  # збереження інформації про пропозицію одруження
        keyboard = types.InlineKeyboardMarkup()
        button_accept = types.InlineKeyboardButton(text='Так', callback_data='accept')
        button_decline = types.InlineKeyboardButton(text='Ні', callback_data='decline')
        keyboard.row(button_accept, button_decline)
        bot.send_message(chat_id,
                         f"Сьогодні {message.from_user.first_name} хоче одружитися з {reply_user.first_name}, чи приймаєш ти його пропозицію руки і серця?",
                         reply_markup=keyboard)

    else:
         bot.send_message(chat_id, "Я не розумію, що ви хочете сказати.")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
   print(call.data)
   chat_id = call.message.chat.id
   user_id = call.from_user.id
   proposal = proposals.get(user_id)
   if proposal is None or proposal['chat_id'] != chat_id or proposal['reply_user_id'] is None:
       bot.answer_callback_query(call.id, text="Ви не можете відповісти на цю пропозицію.", show_alert=True)
       return
   reply_user_id = proposal['reply_user_id']
   reply_user = bot.get_chat_member(chat_id, reply_user_id).user
   if call.data == 'accept':
       bot.send_message(chat_id,
                        f"{reply_user.first_name}, {call.from_user.first_name} погодився одружитися з вами! ❤️")
   elif call.data == 'decline':
       bot.send_message(chat_id, f"{reply_user.first_name}, {call.from_user.first_name} відхилив вашу пропозицію. 😔")
   del proposals[user_id]

@bot.message_handler(commands=['вдуш'])
def handle_shower_command(message):
    current_time = datetime.utcnow().time()
    if current_time >= time(19, 0) and current_time <= time(19, 30):
        bot.reply_to(message, 'Я відійшла в душ')
    else:
        bot.reply_to(message, 'Ця команда доступна лише з 19:00 до 19:30')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.lower() in ['ангел представся', 'ангел представлення', 'ангел хто ти', 'ангел команди']:
        bot.send_message(message.chat.id, 'Привіт, я ангел, я можу спілкуватися з вами або ж виконувати команди такі як:\n\n<b>/від вдарити</b>, \n<b>/від обняти</b>, \n<b>/від поцілувати</b> \n<b>/від образити</b>\n<b>/від чмок</b>\n<b>/від шльоп</b>\n<b>/від сильнийшльоп</b>\n<b>/від кекс або ж /від секс</b>\n<b>/від онанізм</b>\n<b>/від засос</b>\n<b>/стать</b>'
                                          '\n<b>Відповідати на запитання на скільки хтось розумний чи дурний</b>\n<b>Відповідати на запитання так чи ні (В кінці обовязково напиши ?, для прикладу: ангел таке можливе?)</b>\nТакож я маю звичайні команди як:\n\n<b>показати ніжки</b>\n\n<b>А також я можу надавати інформацію про те як купити піар або адмінку, просто пропиши: купити піар, або купити адмінку</b>'
                                          '\nІ хлопчики, будь ласка, будьте зі мною лагідні а також із своїми дівчатками'.format(message.from_user, bot.get_me()),
        parse_mode='html')
        photo_choices = ['static/01.jpg']
        photo = open(random.choice(photo_choices), 'rb')
        bot.send_photo(message.chat.id, photo)
    elif message.text.lower() in ['ангел привіт', 'ангел хай', 'ангел привет']:
        bot.send_message(message.chat.id, 'Привіт')
    elif message.text.lower() in ['ангел як ти?', 'ангел ти як?']:
        bot.send_message(message.chat.id, 'Усе гаразд, а ти як?')
    elif message.text.lower() in ['дякую ангел', 'ангел дякую']:
        bot.send_message(message.chat.id, 'Завжди прошу, кошенятко 😘')
#=================================================================================================================
    elif message.reply_to_message is not None and message.text.lower() == 'ангел скажи наскільки він розумний?':
        bot.send_message(message.chat.id, f"Небеса кажуть що він розумний на {random.randint(0, 100)}%")
    elif message.reply_to_message is not None and message.text.lower() in ['ангел скажи наскільки вона розумна?', 'ангел на скільки вона розумна']:
        bot.send_message(message.chat.id, f"Небеса кажуть що вона розумна на {random.randint(0, 100)}%")
    elif message.reply_to_message is not None and message.text.lower() == 'ангел скажи наскільки він дурний?':
        bot.send_message(message.chat.id, f"Небеса кажуть що він дурний на {random.randint(0, 100)}%")
    elif message.reply_to_message is not None and message.text.lower() == 'ангел скажи наскільки вона дурна?':
        bot.send_message(message.chat.id, f"Небеса кажуть що вона дурна на {random.randint(0, 100)}%")
#======================================================================================================================
    elif message.text.lower().startswith('ангел') and '?' in message.text.lower():
        bot.send_message(message.chat.id, random.choice(['Так', 'Ні']))
    elif message.text.lower().startswith('ангел') and 'хто' in message.text.lower():
        bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто']))

    elif message.text.lower() in ['ангел умнічка', 'ангел ти умнічка', 'ангел ти молодець', 'ангел молодець']:
        bot.send_message(message.chat.id, 'Дякую кошеннятко моє 😍 😘, мені приємно це знати')
    elif message.text.lower() in ['ангел ти тут?', 'ангел ти де', 'ангел ти тут', 'ангел ти де?', 'ангел']:
        bot.send_message(message.chat.id, 'Так я тут, пробач що затримала')
    elif message.text.lower() in ['показати ніжки', 'ніжки', 'ангел покажи ніжки', 'ангел покажи свої ніжки', 'покажи ніжки']:
        bot.send_message(message.chat.id, f"🤗 {message.from_user.first_name} вирішив(-ла) подивитися на ніжки")
        photo_choices = ['static/legs/legs_(1).jpg', 'static/legs/legs_(2).jpg', 'static/legs/legs_(3).jpg',
                     'static/legs/legs_(4).jpg', 'static/legs/legs_(5).jpg', 'static/legs/legs_(6).jpg',
                     'static/legs/legs_(7).jpg', 'static/legs/legs_(8).jpg', 'static/legs/legs_(9).jpg',
                     'static/legs/legs_(10).jpg', 'static/legs/legs_(11).jpg', 'static/legs/legs_(12).jpg',
                     'static/legs/legs_(13).jpg', 'static/legs/legs_(14).jpg', 'static/legs/legs_(15).jpg',
                     'static/legs/legs_(16).jpg', 'static/legs/legs_(17).jpg', 'static/legs/legs_(18).jpg',
                     'static/legs/legs_(19).jpg', 'static/legs/legs_(20).jpg', 'static/legs/legs_(21).jpg',
                     'static/legs/legs_(22).jpg', 'static/legs/legs_(23).jpg', 'static/legs/legs_(24).jpg',
                     'static/legs/legs_(25).jpg', 'static/legs/legs_(26).jpg', 'static/legs/legs_(27).jpg',
                     'static/legs/legs_(28).jpg', 'static/legs/legs_(29).jpg', 'static/legs/legs_(30).jpg',
                     'static/legs/legs_(31).jpg', 'static/legs/legs_(32).jpg']
        photo_path = random.choice(photo_choices)
        with open(photo_path, 'rb') as photo_file:
            bot.send_photo(message.chat.id, photo_file)
    elif message.text.lower() in ['купити адмінку', 'купити рекламу', 'купити піар', 'піар']:
        bot.send_message(message.chat.id, 'ОУУУ чудова ідея, тоді ось тоюбі інформація:\n'
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

bot.polling(none_stop=True)