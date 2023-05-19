import random
import re
import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

angel = ['ангелятко', 'ангел', 'ангелику', 'ангелочок']

def handle_commands(bot, message):
    text = message.text.lower()

    hello = {"ангел привіт", "ангел здоров", "ангел хай"}
    how_are_you = {"ангел як справи", "ангел ти як"}
    how_are_you_second = {"як справи", "ти як", "як ти", "як ся маєш", "як", "", ""}

    if any(command in text for command in hello):
        bot.send_message(message.chat.id, "Привіт хлопче!")
    elif any(command in text for command in how_are_you):
        if any(command in text for command in hello | how_are_you_second):
            bot.send_message(message.chat.id, "Привіт, усе добре, а в тебе?")  
        elif "доречі привіт" in text:
            bot.send_message(message.chat.id, "Привіт, усе добре, а в тебе?")
        else:
            bot.send_message(message.chat.id, "Усе добре, а в тебе?")
    else: 
# else
        text = message.text.lower()
        answered_question = False
        for keyword in angel:
            if text == f"{keyword} представся" or text == f"{keyword} представлення" or text == f"{keyword} хто ти" or text == f"{keyword} команди" or text == f"{keyword} що вмієш":
                bot.send_message(message.chat.id,
                                 'Привіт, я ангел, я можу спілкуватися з вами або ж виконувати команди такі як:'
                                 '\n\n<b>/від вдарити</b>, \n<b>/від обняти</b>, \n<b>/від поцілувати</b> \n<b>/від образити</b>'
                                 '\n<b>/від чмок</b>\n<b>/від шльоп</b>\n<b>/від сильнийшльоп</b>\n<b>/від кекс або ж /від секс</b>\n<b>/від онанізм</b>'
                                 '\n<b>/від засос</b>\n<b>/стать</b>'
                                 '\n<b>Відповідати на запитання на скільки хтось розумний чи дурний</b>\n<b>Відповідати на запитання так чи ні '
                                 '(В кінці обовязково напиши ?, для прикладу: ангел таке можливе?)</b>\n\nТакож я маю звичайні команди як:'
                                 '\n\n<b>показати ніжки</b>\n\n<b>А також я можу надавати інформацію про те як купити піар або адмінку, просто '
                                 'пропиши: купити піар, або купити адмінку</b>\n\nА і ще одне, з 19:00 до 19:30 я іду в душ, кожного дня, тому хлопчики - '
                                 'не заглядати, а то покараю\n'
                                 '\nІ хлопчики, будь ласка, будьте зі мною лагідні а також із своїми дівчатками'.format(
                                     message.from_user, bot.get_me()),
                                 parse_mode='html')
                photo_choices = ['static/01.jpg']
                photo = open(random.choice(photo_choices), 'rb')
                bot.send_photo(message.chat.id, photo)
            #        elif text in [f"{keyword} привіт", f"{keyword} привет", f"{keyword} хай", f"{keyword} здоров"]:
            #        bot.send_message(message.chat.id, 'Привіт')
            elif text in [f"{keyword} як ти", f"{keyword} як справи", f"{keyword} ти як", f"{keyword} як ти?",
                          f"{keyword}, ти як", f"{keyword}, ти як?"]:
                bot.send_message(message.chat.id, 'Усе гаразд, а ти як?')
            elif text == f"{keyword} дякую" or text == f"дякую {keyword}":
                bot.send_message(message.chat.id, 'Завжди прошу, моє кошенятко 😘')
            # elif text == f"{keyword} що ти вмієш?" or text == f"{keyword} що ти можеш?":
            #    bot.send_message(message.chat.id, 'Я можу відповісти на твої запитання, показати картинки, розповісти анекдоти і багато іншого!')
            # elif text == f"{keyword} допоможи" or text == f"{keyword} допоможи мені":
            #    bot.send_message(message.chat.id, 'Звісно, що допоможу! Що тобі потрібно?')
            # elif text == f"{keyword} дай пораду" or text == f"{keyword} порадь":
            #    bot.send_message(message.chat.id, 'Моя порада: будь завжди веселим і позитивним!')
            elif text == f"{keyword} до побачення" or text == f"{keyword} бувай":
                bot.send_message(message.chat.id, 'До зустрічі! Бувай ❤')
            elif text == f"{keyword} на добраніч" or text == f"{keyword} спокійної ночі" or text == f"{keyword} надобраніч":
                bot.send_message(message.chat.id, 'На добраніч моє кошеня 😘❤')
            elif text == f"{keyword} вірш" or text == f"{keyword} поезія":
                bot.send_message(message.chat.id,
                                 'А ось і мій вірш:\nТи мій ангел, що з неба злетів,\nЩоб мені допомогти в біді,\nЗавжди поруч, коли я сам,\nТи мій ангел, мій друг і мій брат.')
            # =================================================================================================================
            # elif message.reply_to_message is not None and message.text.lower() == 'ангел скажи наскільки він розумний':
            #    bot.send_message(message.chat.id, f"Небеса кажуть що він розумний на {random.randint(0, 100)}%")
            # elif message.reply_to_message is not None and message.text.lower() in ['ангел скажи наскільки вона розумна', 'ангел на скільки вона розумна']:
            #    bot.send_message(message.chat.id, f"Небеса кажуть що вона розумна на {random.randint(0, 100)}%")
            # elif message.reply_to_message is not None and message.text.lower() == 'ангел скажи наскільки він дурний?':
            #    bot.send_message(message.chat.id, f"Небеса кажуть що він дурний на {random.randint(0, 100)}%")
            # elif message.reply_to_message is not None and message.text.lower() == 'ангел скажи наскільки вона дурна?':
            #    bot.send_message(message.chat.id, f"Небеса кажуть що вона дурна на {random.randint(0, 100)}%")
            # ======================================================================================================================
            elif text.startswith(f"{keyword} ") and '?' in text:
                bot.send_message(message.chat.id, random.choice(['Так', 'Ні']))
            elif text.startswith(f"{keyword}") and 'хто' in text:
                bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто']))
            elif re.search(r"\bангел\b.*\bскільки\b.*\bразів\b.*\bтиждень\b.*[.?!]", text,
                           re.IGNORECASE) and not answered_question:
                bot.send_message(message.chat.id, 'Десь ' + str(random.randint(1, 10)))
                answered_question = True
            elif text == f"{keyword} ти умнічка" or text == f"{keyword} ти молодець" or text == f"{keyword} розумниця" or text == f"{keyword} умнічка" or text == f"{keyword} молодець" or text == f"{keyword} найкраща" or text == f"{keyword} найкраща!" or text == f"{keyword} - найкраща!" or text == f"{keyword} - найкраща" or text == f"{keyword} ти найкраща" or text == f"{keyword} ти найкраща!":
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
