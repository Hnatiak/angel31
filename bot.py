# -*- coding: utf-8 -*-

import json
import python_weather
import asyncio
import os
import types
import telebot
import config
import random
import logging
from telebot import TeleBot, types
from datetime import datetime, timedelta
import time
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from games import bot, start_number_game, start_number_game_with_attempts, guess_number, end_number_game, start_word_game, play_word_game, end_word_game
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

with open('commands.json', 'r', encoding='utf-8') as file:
    commands_data = json.load(file)
    
    
# async def get_weather(city_name):
#     async with python_weather.Client(unit=python_weather.METRIC) as client:
#         weather = await client.get(city_name)
#         return weather

# def get_weather_info(city_name):
#     if os.name == 'nt':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     return asyncio.run(get_weather(city_name))

# @bot.message_handler(commands=['погода'])
# def handle_weather(message):
#     city_name = message.text[len('/погода '):].strip()
#     if not city_name:
#         bot.send_message(message.chat.id, "Будь ласка, введіть назву міста.")
#         return
    
#     try:
#         weather = get_weather_info(city_name)
#         if weather.country:
#             weather_info = (
#                 f"Місто: {weather.country}\n"
#                 f"Дата: {weather.datetime}\n"
#                 f"Температура: {weather.temperature}°C\n"
#                 f"Вологість: {weather.humidity}°F\n"
#                 f"Швидкість вітру: {weather.wind_speed}\n"
#                 f"Опис: {weather.description}"
#             )
#             bot.send_message(message.chat.id, weather_info)
#         else:
#             bot.send_message(message.chat.id, "Не вдалося знайти інформацію про погоду для цього міста.")
#     except Exception as e:
#         logger.error(f"Error handling weather command: {e}")
#         bot.send_message(message.chat.id, "Сталася помилка під час отримання інформації про погоду.")




# async def get_weather(city_name):
#     async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
#         weather = await client.get(city_name)
#         return weather

# def convert_f_to_c(fahrenheit):
#     return round((fahrenheit - 32) * 5.0/9.0)

# def get_weather_info(city_name):
#     if os.name == 'nt':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     return asyncio.run(get_weather(city_name))

# @bot.message_handler(commands=['погода'])
# def handle_weather(message):
#     city_name = message.text[len('/погода '):].strip()
#     if not city_name:
#         bot.send_message(message.chat.id, "Будь ласка, введіть назву міста.")
#         return
    
#     try:
#         weather = get_weather_info(city_name)
#         if weather.country:
#             temperature_celsius = convert_f_to_c(weather.temperature)
#             weather_info = (
#                 f"Температура: {temperature_celsius}°C\n"
#                 f"Опис: {weather.description}"
#             )
#             bot.send_message(message.chat.id, weather_info)
#         else:
#             bot.send_message(message.chat.id, "Не вдалося знайти інформацію про погоду для цього міста.")
#     except Exception as e:
#         logger.error(f"Error handling weather command: {e}")
#         bot.send_message(message.chat.id, "Сталася помилка під час отримання інформації про погоду.")
    
  
    
# =====================================================================================================================================================================
# ПОЧАТКОВІ КОМАНДИ
# =====================================================================================================================================================================

def process_command(message):
    command_text = message.text.lower().split()[0]

    for command in commands_data['commands']:
        if command_text == '/' + command['command']:
            sender = message.from_user.first_name
            bot_name = bot.get_me().first_name

            if 'answer_bot' in command:
                reply = command['answer_bot'].format(sender=sender, bot=bot_name)
                bot.send_message(message.chat.id, reply, parse_mode='HTML')

            photos = command.get('photos', [])
            for photo_path in photos:
                with open(photo_path, 'rb') as photo_file:
                    bot.send_photo(message.chat.id, photo_file)

            return

    bot.reply_to(message, "Невідома команда. Спробуйте ще раз.")
    
@bot.message_handler(commands=['start', 'команди', 'формати-запитання', 'ігри'])  # Додаткові команди, які обробляються безпосередньо
def handle_commands(message):
    process_command(message)
    
    
# =====================================================================================================================================================================
# РОЗМОВА З БОТОМ
# =====================================================================================================================================================================

angel = ['ангелятко', 'ангел', 'ангелику', 'ангелочок']

@bot.message_handler(func=lambda message: any(message.text.lower().startswith(keyword) for keyword in angel))
def handle_commands(message):
    text = message.text.lower()
    sender = message.from_user.first_name

    for keyword in angel:
        if text.startswith(keyword):
            text_after_keyword = text[len(keyword):].strip()
            break
    
    answered_question = False

    for command in commands_data['speak_with_bot']:
        for keyword in command['say']:
            if keyword in text_after_keyword:
                answer = command['answer']
                bot_name = bot.get_me().first_name
                
                if isinstance(answer, list):
                    chosen_answer = random.choice(answer)
                    if '{sender}' in chosen_answer:
                        reply = chosen_answer.format(sender=sender)
                    else:
                        reply = chosen_answer.format(bot=bot_name)
                else:
                    if '{sender}' in answer:
                        reply = answer.format(sender=sender)
                    else:
                        reply = answer
                
                bot.reply_to(message, reply)
                answered_question = True

                photos = command.get('photos', [])
                if photos:
                    photo_path = random.choice(photos)
                    with open(photo_path, 'rb') as photo_file:
                        bot.send_photo(message.chat.id, photo_file)

                return

    if not answered_question:
        if text_after_keyword in ["скажи наскільки він розумний?", "скажи наскільки він розумний", "напиши наскільки він розумний", "як ти думаєш наскільки він розумний", "напиши наскільки він розумний?", "як ти думаєш наскільки він розумний?"]:
            bot.send_message(message.chat.id, f"Небеса кажуть що він розумний на {random.randint(0, 100)}%")
            answered_question = True
        elif text_after_keyword in ["скажи наскільки вона розумна?", "скажи наскільки вона розумна", "напиши наскільки вона розумна", "як ти думаєш наскільки вона розумна", "напиши наскільки вона розумна?", "як ти думаєш наскільки вона розумна?"]:
            bot.send_message(message.chat.id, f"Небеса кажуть що вона розумна на {random.randint(0, 100)}%")
            answered_question = True
        elif text_after_keyword in ["скажи наскільки він дурний?", "скажи наскільки він дурний", "напиши наскільки він дурний", "як ти думаєш наскільки він дурний", "напиши наскільки він дурний?", "як ти думаєш наскільки він дурний?"]:
            bot.send_message(message.chat.id, f"Небеса кажуть що він дурний на {random.randint(0, 100)}%")
            answered_question = True
        elif text_after_keyword.startswith('хто') and '?' in text_after_keyword:
            bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто', 'Він/Вона']))
            answered_question = True
        elif text_after_keyword.startswith('він чи я') and '?' in text_after_keyword:
            bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто з вас', 'Він', 'Ви обоє']))
            answered_question = True
        elif text_after_keyword.startswith('вона чи я') and '?' in text_after_keyword:
            bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто з вас', 'Вона', 'Ви обоє']))
            answered_question = True
        elif re.search(r"\bскільки\b.*\bразів\b.*\bтиждень\b", text_after_keyword):
            bot.send_message(message.chat.id, 'Десь ' + str(random.randint(1, 10)) + ' разів на тиждень')
            answered_question = True
        elif text_after_keyword in ['правда чи дія?', 'правда чи дія?']:
            bot.send_message(message.chat.id, random.choice(['Правда', 'Дія']))
            answered_question = True
        elif '?' in text_after_keyword:
            bot.send_message(message.chat.id, random.choice(['Так', 'Ні']))
            answered_question = True
        elif r'\b.*' in text_after_keyword:
            bot.send_message(message.chat.id, random.choice(['Так', 'Ні', 'Мабуть', 'Можливо', 'Не думаю', 'Не думаю, але можливо']))
            answered_question = True
        else:
            bot.reply_to(message, "Вибач, я не розумію твого запиту.")


# =====================================================================================================================================================================
# ІГРИ
# =====================================================================================================================================================================

@bot.message_handler(commands=['гра_в_цифри'])
def handle_start_number_game(message):
    start_number_game(message)

@bot.message_handler(commands=['гра_в_цифри_10', 'гра_в_цифри_9', 'гра_в_цифри_8', 'гра_в_цифри_7', 'гра_в_цифри_6', 'гра_в_цифри_5', 'гра_в_цифри_4', 'гра_в_цифри_3', 'гра_в_цифри_2', 'гра_в_цифри_1'])
def handle_start_number_game_with_attempts(message):
    start_number_game_with_attempts(message)

@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_guess_number(message):
    guess_number(message)

@bot.message_handler(commands=['закінчити_гру_в_цифри'])
def handle_end_number_game(message):
    end_number_game(message)

@bot.message_handler(commands=['гра_в_слова'])
def handle_start_word_game(message):
    start_word_game(message)

@bot.message_handler(func=lambda message: re.match(r'^[а-яіїєґ]+$', message.text, re.IGNORECASE) is not None)
def handle_play_word_game(message):
    play_word_game(message)

@bot.message_handler(commands=['закінчити_гру_в_слова'])
def handle_end_word_game(message):
    end_word_game(message)


# =====================================================================================================================================================================
# СТАТЬ
# =====================================================================================================================================================================

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

# =====================================================================================================================================================================
# /ВІД КОМАНДИ
# =====================================================================================================================================================================

@bot.message_handler(commands=['від'])
def handle_command_vid(message):
    words = message.text.lower().split()
    if len(words) < 2:
        bot.reply_to(message, "Виберіть дію щоб виконати цю команду")
        return

    action_text = words[1]
    target = message.reply_to_message.from_user if message.reply_to_message else None
    if not target:
        bot.reply_to(message, "Виберіть користувача щоб виконати цю команду")
        return

    reason = ' '.join(words[2:]) if len(words) > 2 else ''
    
    try:
        for action in commands_data['actions']:
            if action_text in action['action']:
                reply = action['message_template'].format(sender=message.from_user.first_name, receiver=target.first_name, reason=reason)
                bot.send_message(message.chat.id, reply)
                
                photos = action.get('photos', [])
                if photos:
                    photo_path = random.choice(photos)
                    if photo_path.endswith('.gif'):
                        with open(photo_path, 'rb') as photo_file:
                            bot.send_animation(message.chat.id, photo_file)
                    else:
                        with open(photo_path, 'rb') as photo_file:
                            bot.send_photo(message.chat.id, photo_file)
                else:
                    print("No photos found for action:", action_text)
                
                return

        bot.reply_to(message, "Невідома команда. Спробуйте ще раз.")
    
    except telebot.apihelper.ApiTelegramException as e:
        if e.error_code == 429:
            retry_after = int(e.result_json['parameters']['retry_after'])
            print(f"Too Many Requests: Retry after {retry_after} seconds | Було сильне перевантаження на сервер, потрібно зачекати {retry_after} секунд")
        else:
            print(f"Telegram API Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# =====================================================================================================================================================================
# Щось ДЛЯ ОДРУЖЕННЯ
# =====================================================================================================================================================================

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

# =====================================================================================================================================================================
# ДОДАТКОВІ ФОКУСИ
# =====================================================================================================================================================================

angel = ['ангелятко', 'ангел', 'ангелику', 'ангелочок']
insult = {'дура', 'дурак', 'ідіот', 'лох', 'дибілка', 'ідіотка', 'тварь', 'сядешь мені на хуй', 'піди нахуй', 'від сосешь мені', 'відсосешь мені', 'та пошел ты нахуй', 'сядь мені на хуй', 'пошла на хуй', 'ти сосешь', 'станеш раком', 'стань раком', 'дибіл', 'дебіл', 'дебілка', 'дурна', 'гей', 'лесбіянка', 'лисбіянка', 'самий уйобний бот', 'иди нахуй', 'будеш сосать члена', 'будеш сосать', 'сосать', 'соси', 'соси член', 'йди нахуй', 'іді нахуй', 'йди до сраки', 'іди до сраки', 'хуй', 'пизда', 'піздец', 'пиздец', 'йди в пізду'}


@bot.message_handler(func=lambda message: any(word in message.text.lower() for word in insult) and any(word in message.text.lower() for word in ["ангел ти", "особа ти", "ангел", 'ангел ', 'Ангел ', 'Ангел', 'Ангел ти ', '']))
def handle_insult(message):
    try:
        bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=int((datetime.now() + timedelta(minutes=1)).timestamp()))
        user_mention = f"@{message.from_user.username}" if message.from_user.username else sender
        bot.send_message(message.chat.id, f"мут 1 хвилину {user_mention}", reply_to_message_id=message.message_id)
        bot.reply_to(message, "Тепер подумай над своєю поведінкою")
    except Exception as e:
        bot.send_message(message.chat.id, "Мені взагаліто не приємно")


# =====================================================================================================================================================================
# /ВДУШ
# ===================================================================================================================================================================== 
# is_shower_time = False

# def current_time():
#     return time.strftime("%H:%M:%S", time.localtime())

# @bot.message_handler(commands=['вдуш'])
# def handle_shower_command(message):
#     global is_shower_time

#     current_hour = int(time.strftime("%H", time.localtime()))

#     if current_hour == 19:
#         is_shower_time = True
#         bot.send_message(message.chat.id, 'Я відійшла в душ, тому тепер всі команди будуть не доступні (/вдуш). Я повернусь через 30 хвилин.')

#         start_time = time.time()

#         while time.time() - start_time <= 1800:
#             time.sleep(1)

#         bot.send_message(message.chat.id, 'Фух, все, я прийняла душ. Отже, що тепер робитимемо?')

#         try:
#             user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
#             bot.send_message(message.chat.id, f"Мут на 1 хвилину для {user_mention}", reply_to_message_id=message.message_id)
#             bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=int(time.time()) + 60)
#             bot.reply_to(message, "НАВІЩО ТИ НАМАГАВСЯ ПІДГЛЯНУТИ ЗА МНОЮ КОЛИ Я ПРИЙМАЛА ДУШ? Тепер посиди і подумай що ти накоїв!")
#         except Exception as e:
#             bot.send_message(message.chat.id, "Блінчик, ну прошу, не ргоби так більше, мені це неприємно 🥺")

#         is_shower_time = False
#     else:
#         bot.reply_to(message, 'Ця команда доступна лише о 19:00')

# def auto_shower():
#     global is_shower_time

#     start_time = time.time()

#     while True:
#         current_hour = int(time.strftime("%H", time.localtime()))

#         if current_hour == 19 and not is_shower_time and time.time() - start_time <= 1800:
#             is_shower_time = True
#             bot.send_message(chat_id, 'Доброго вечора, пішла в душ. Повернусь через 30 хвилин.')

#             shower_start_time = time.time()

#             while time.time() - shower_start_time <= 1800:
#                 time.sleep(1)

#             bot.send_message(chat_id, 'Все, я вже прийшла з душу душ. Тепер всі команди знову доступні. Отже з чого розпочнемо?')

#             is_shower_time = False

#         time.sleep(60)

# auto_shower()



# =====================================================================================================================================================================
# ПОГОДА
# =====================================================================================================================================================================




# =====================================================================================================================================================================
# ПЕРЕКЛАД З АНГЛ НА УКР
# =====================================================================================================================================================================

translate_dict = {}
if 'translation_dict' in commands_data:
    translate_dict = commands_data['translation_dict'][0]

def translate_word(word):
    if word in translate_dict:
        return translate_dict[word]
    else:
        return word

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    player_id = message.from_user.id
    text = message.text.lower()
    words = re.findall(r'\b\w+\b', text)

    translated_words = []
    for word in words:
        ukrainian_word = translate_word(word)
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

bot.polling(none_stop=True)