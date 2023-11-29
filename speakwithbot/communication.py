import random
import re
import telebot
import config
import requests

bot = telebot.TeleBot(config.TOKEN)

angel = [ 'ангелятко', 'ангел', 'ангелику', 'ангелочок' ]

whereareyou = ["Так я тут, пробач що затримала", "Я тут", "Я завжди на місці, не хвилюйся.", "Вибач, я тут. Все добре!", "Ти тут, і це головне. І я також на зв'язку." ]

whatimdoing = [ "обновлюю базу даних", "доповнюю свої функції", "нічого такого", "чекаю твоїх вказвок", "відпочиваю", "виправляю помилки", "роблю тести над обновленнями" ]

random_response_whatimdoing = random.choice(whatimdoing)



# @bot.message_handler(func=lambda message: any(keyword in message.text.lower() for keyword in angel))
def handle_commands(bot, message):
    text = message.text.lower()

    hello = {"ангел привіт", "ангел здоров", "ангел хай", "ангел дарова", "ангел здоров", "ангел хелоу", "ангел хай", "ангел салют", "ангел салю"}
    how_are_you = {"ангел як справи", "ангел ти як", "ангел як почуваєшся"}
    how_are_you_second = {"як справи", "ти як", "як ти", "як ся маєш", "як", "", ""}

    if any(command in text for command in hello):
        bot.send_message(message.chat.id, "Привіт!")
    elif any(command in text for command in how_are_you):
        if "доречі привіт" in text:
            bot.send_message(message.chat.id, "Привіт, усе добре, а в тебе?")
        else:
            bot.send_message(message.chat.id, "Усе добре, а в тебе?")
#     elif any(command in text for command in hello | how_are_you_second):
#         bot.send_message(message.chat.id, "Привіт, усе добре, а в тебе?")
    if re.search(r"\bангел число від (\d+) до (\d+)\b", text, re.IGNORECASE):
        match = re.search(r"\bангел число від (\d+) до (\d+)\b", text, re.IGNORECASE)
        start_num = int(match.group(1))
        end_num = int(match.group(2))

        if start_num <= end_num:
            bot.send_message(message.chat.id, str(random.randint(start_num, end_num)))
        else:
            bot.send_message(message.chat.id, "Перепрошую, але наступне число, яке ви вказали, не є більше " + str(start_num))
    else:
# else
        text = message.text.lower()
        answered_question = False
        for keyword in angel:
            if text == f"{keyword} представся" or text == f"{keyword} представлення" or text == f"{keyword} хто ти" or text == f"{keyword} команди" or text == f"{keyword} що вмієш" or text == f"{keyword} що ти можеш" or text == f"{keyword} та що ти можеш" or text == f"{keyword} що вмієш?" or text == f"{keyword} що ти вмієш?" or text == f"{keyword} хто ти?" or text == f"{keyword} що ти можеш?" or text == f"{keyword} та що ти можеш?":
                bot.send_message(message.chat.id,
                                 'Привіт, я ангел, я можу спілкуватися з вами або ж виконувати команди такі як:'
                                 '\n\n<b>/від вдарити</b>, \n<b>/від обняти</b>, \n<b>/від поцілувати</b> \n<b>/від образити</b>'
                                 '\n<b>/від чмок</b>\n<b>/від шльоп</b>\n<b>/від сильнийшльоп</b>\n<b>/від кекс або ж /від секс</b>\n<b>/від онанізм</b>'
                                 '\n<b>/від засос</b>\n<b>/стать</b>'
                                 '\n<b>Відповідати на запитання на скільки хтось розумний чи дурний</b>\n<b>Відповідати на запитання так чи ні '
                                 '(В кінці обовязково напиши ?, для прикладу: ангел таке можливе?)</b>\n\nТакож я маю звичайні команди як:'
                                 '\n\n<b>показати ніжки</b>\n\n<b>А також я можу надавати інформацію про те як купити піар або адмінку, просто '
                                 'пропиши: купити піар, або купити адмінку</b>\n\nТакож у мене є ігри як:\n\n/гра_в_цифри\n\nА і ще одне, з 19:00 до 19:30 я іду в душ, кожного дня, тому хлопчики - '
                                 'не заглядати, а то покараю\n'
                                 '\nІ хлопчики, будь ласка, будьте зі мною лагідні а також із своїми дівчатками'.format(
                                     message.from_user, bot.get_me()),
                                 parse_mode='html')
                photo_choices = ['static/01.jpg']
                photo = open(random.choice(photo_choices), 'rb')
                bot.send_photo(message.chat.id, photo)
            elif text in [f"{keyword} як ти", f"{keyword} як справи", f"{keyword} ти як", f"{keyword} як ти?", f"{keyword}, ти як", f"{keyword}, ти як?"]:
                bot.send_message(message.chat.id, 'Усе гаразд, а ти як?')
            elif text == f"{keyword} дякую" or text == f"дякую {keyword}":
                bot.send_message(message.chat.id, 'Завжди прошу, моє кошенятко 😘')
            elif text == f"{keyword} дай пораду" or text == f"{keyword} порадь":
               bot.send_message(message.chat.id, 'Моя порада: будь завжди веселим і позитивним!')
            elif text == f"{keyword} факт":
                responses = [
                    'Факт: Історично Україна існує з 1187 року, тоді як Росія сформувалася в XV (15) столітті.',
                    'Факт: Україна існує з 1187 року, тобто довше, ніж Росія, яка з\'явилася лише в XV (15) столітті.',
                    'Факт: Походження української мови – окрема тема для статті! Точно сказати, коли зародилася українська мова, складно, але відомо, що вона однозначно виникла раніше за російську, німецьку, турецьку тощо. За даними вченого Василя Кобилюха, наша мова сформувалася ще в IV-Х (4-5) тисячоліттях до нашої ери і походить вона зі санскриту (це стародавня мова, яка належить до гілки індоарійських мов).',
                    'Факт: Перші слова з української мови були записані в 448 р. н.е. Тоді візантійський історик Пріск Панікійський перебував на території сучасної України в таборі володаря Аттіли, який згодом розгромив Римську імперію, і записав слова “мед” і “страва”.',
                    'Факт: На відміну від решти східнослов’янських мова, іменник в українській має 7 відмінків. Як ви зрозуміли, вирізняє нас кличний відмінок, який існує також в латині, грецькій та санскритській граматиках',
                    'Факт: У “Короткому словнику синонімів української мови”, де зібрано 4279 синонімічних рядів, найбільше синонімів має слово “бити” – аж 45!',
                    'Факт: Ви ніколи не замислювалися над тим, що в нашій мові є три форми майбутнього часу! Цікавий матеріал, чи не так? Нумо згадувати разом – проста (піду), складна (йтиму) і складена (буду йти).',
                    'Факт: Однією з “родзинок” української мови є те, що вона багата на зменшувальні форми. Навіть слово “вороги” має зменшувально-пестливу форму, яка вживається в гімні України. Пам’ятаєте: “…згинуть наші вороженьки, як роса на сонці”.',
                    'Факт: Українську мову офіційно визнали літературною після видання “Енеїди” Івана Котляревського. Відтак, Котляревського вважають основоположником нової української мови.',
                ]
                random_response = random.choice(responses)
                bot.send_message(message.chat.id, random_response)
            elif text == f"{keyword} гімн україни" or text == f"{keyword} гім України":
                bot.send_message(message.chat.id, 'Ще не вмерла України і слава, і воля,\nЩе нам, браття молодії, усміхнеться доля.\nЗгинуть наші воріженьки, як роса на сонці,\nЗапануєм і ми, браття, у своїй сторонці.\n\nДушу й тіло ми положим за нашу свободу,\nІ покажем, що ми, браття, козацького роду!')
            elif text == f"{keyword} Слава Україні" or text == f"{keyword} слава україні" or text == f"{keyword} слава Україні" or f"{keyword} Слава Україні!" or f"{keyword} Слава україні!" or text == f"{keyword} слава україні!" or text == f"{keyword} слава Україні!" or text == f"{keyword} Слава україні!":
                bot.send_message(message.chat.id, 'Героям Слава!')
            elif text == f"{keyword} до побачення" or text == f"{keyword} бувай":
                bot.send_message(message.chat.id, 'До зустрічі! Бувай ❤')
            elif text == f"{keyword} на добраніч" or text == f"{keyword} спокійної ночі" or text == f"{keyword} надобраніч":
                bot.send_message(message.chat.id, 'На добраніч моє кошеня 😘❤')
            elif text == f"{keyword} вірш" or text == f"{keyword} поезія":
                bot.send_message(message.chat.id,
                                 'А ось і мій вірш:\nТи мій ангел, що з неба злетів,\nЩоб мені допомогти в біді,\nЗавжди поруч, коли я сам,\nТи мій ангел, мій друг і мій брат.')

            elif text == f"{keyword} скажи наскільки він розумний?" or text == f"{keyword} скажи наскільки він розумний" or text == f"{keyword} напиши наскільки він розумний" or text == f"{keyword} як ти думаєш наскільки він розумний" or text == f"{keyword} напиши наскільки він розумний?" or text == f"{keyword} як ти думаєш наскільки він розумний?":
               bot.send_message(message.chat.id, f"Небеса кажуть що він розумний на {random.randint(0, 100)}%")
            elif text == f"{keyword} скажи наскільки вона розумна?" or text == f"{keyword} скажи наскільки вона розумна" or text == f"{keyword} напиши наскільки вона розумна" or text == f"{keyword} як ти думаєш наскільки вона розумна" or text == f"{keyword} напиши наскільки вона розумна?" or text == f"{keyword} як ти думаєш наскільки вона розумна?":
               bot.send_message(message.chat.id, f"Небеса кажуть що вона розумна на {random.randint(0, 100)}%")
            elif text == f"{keyword} скажи наскільки він дурний?" or text == f"{keyword} скажи наскільки він дурний" or text == f"{keyword} напиши наскільки він дурний" or text == f"{keyword} як ти думаєш наскільки він дурний" or text == f"{keyword} напиши наскільки він дурний?" or text == f"{keyword} як ти думаєш наскільки він дурний?":
               bot.send_message(message.chat.id, f"Небеса кажуть що він дурний на {random.randint(0, 100)}%")
                
            elif text.startswith(f"{keyword}") and 'хто' in text:
                bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто', 'Він/Вона']))
            elif text.startswith(f"{keyword}") and 'він чи я' in text:
                bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто з вас', 'Він', 'Ви обоє']))
            elif text.startswith(f"{keyword}") and 'вона чи я' in text:
                bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто з вас', 'Вона', 'Ви обоє']))
            # elif re.search(fr"\b{keyword}\b.*\bскільки\b.*\bразів\b.*\bтиждень\b", text, re.IGNORECASE) and not answered_question:
            #     bot.send_message(message.chat.id, 'Десь ' + str(random.randint(1, 10)) + ' разів на тиждень')
            #     answered_question = True
            elif re.search(fr"\b{keyword}\b.*\bскільки\b.*\bразів\b.*\bтиждень\b", text, re.IGNORECASE) and not answered_question:
                bot.send_message(message.chat.id, 'Десь ' + str(random.randint(1, 10)) + ' разів на тиждень')
                answered_question = True
            elif text == f"{keyword} ти умнічка" or text == f"{keyword} ти молодець" or text == f"{keyword} розумниця" or text == f"{keyword} умнічка" or text == f"{keyword} молодець" or text == f"{keyword} найкраща" or text == f"{keyword} найкраща!" or text == f"{keyword} - найкраща!" or text == f"{keyword} - найкраща" or text == f"{keyword} ти найкраща" or text == f"{keyword} ти найкраща!" or text == f"{keyword} ти сонечко" or text == f"{keyword} ти молодчина":
                bot.send_message(message.chat.id, 'Дякую кошеннятко моє 😍 😘, мені приємно це знати')
            elif text == f"{keyword}" or text == f"{keyword} ти тут" or text == f"{keyword} ти де" or text == f"{keyword} ти тут?" or text == f"{keyword} ти де?":
                random_response = random.choice(whereareyou)
                bot.send_message(message.chat.id, random_response)
            elif any(command in text for command in [ f"{keyword} що поробляєш", f"{keyword} що робиш", f"{keyword} чим займаєшся?", f"{keyword} чим займаєшся", f"{keyword} чим ти займаєшся", f"{keyword} що ти робиш", f"{keyword} що робиш?", f"{keyword} що поробляєш?", f"{keyword} що ти поробляєш?", f"{keyword} що ти поробляєш"]):
                random_response_whatimdoing = random.choice(whatimdoing)  # Generate a new random response
                bot.send_message(message.chat.id, random_response_whatimdoing)
            elif text.startswith(f"{keyword} ") and '?' in text:
                bot.send_message(message.chat.id, random.choice(['Так', 'Ні']))
            elif text == "показати ніжки" or text == "ніжки" or text == f"{keyword} покажи ніжки" or text == f"{keyword} покажи свої ніжки" or text == f"покажи ніжки":
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
    # else:
    #     bot.send_message(message.chat.id, "Я не розумію тебе")
    
    
if __name__ == '__main__':
    bot.polling(none_stop=True)
