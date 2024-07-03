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

if random_response_whatimdoing == "відпочиваю":
    bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто', 'Він/Вона']))
elif text == f"{keyword} вірш" or text == f"{keyword} поезія":
    bot.send_message(message.chat.id, 'А ось і мій вірш:\nТи мій ангел, що з неба злетів,\nЩоб мені допомогти в біді,\nЗавжди поруч, коли я сам,\nТи мій ангел, мій друг і мій брат.')
elif text == f"{keyword} скажи наскільки він розумний?" or text == f"{keyword} скажи наскільки він розумний" or text == f"{keyword} напиши наскільки він розумний" or text == f"{keyword} як ти думаєш наскільки він розумний" or text == f"{keyword} напиши наскільки він розумний?" or text == f"{keyword} як ти думаєш наскільки він розумний?":
    bot.send_message(message.chat.id, f"Небеса кажуть що він розумний на {random.randint(0, 100)}%")
elif text == f"{keyword} скажи наскільки вона розумна?" or text == f"{keyword} скажи наскільки вона розумна" or text == f"{keyword} напиши наскільки вона розумна" or text == f"{keyword} як ти думаєш наскільки вона розумна" or text == f"{keyword} напиши наскільки вона розумна?" or text == f"{keyword} як ти думаєш наскільки вона розумна?":
    bot.send_message(message.chat.id, f"Небеса кажуть що вона розумна на {random.randint(0, 100)}%")
elif text == f"{keyword} скажи наскільки він дурний?" or text == f"{keyword} скажи наскільки він дурний" or text == f"{keyword} напиши наскільки він дурний" or text == f"{keyword} як ти думаєш наскільки він дурний" or text == f"{keyword} напиши наскільки він дурний?" or text == f"{keyword} як ти думаєш наскільки він дурний?":
    bot.send_message(message.chat.id, f"Небеса кажуть що він дурний на {random.randint(0, 100)}%")
elif text.startswith(f"{keyword}") and 'хто' and '?' in text:
    bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто', 'Він/Вона']))
elif text.startswith(f"{keyword}") and 'він чи я' and '?' in text:
    bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто з вас', 'Він', 'Ви обоє']))
elif text.startswith(f"{keyword}") and 'вона чи я' in text:
    bot.send_message(message.chat.id, random.choice(['Ти', 'Ніхто з вас', 'Вона', 'Ви обоє']))
# elif re.search(fr"\b{keyword}\b.*\bскільки\b.*\bразів\b.*\bтиждень\b", text, re.IGNORECASE) and not answered_question:
#     bot.send_message(message.chat.id, 'Десь ' + str(random.randint(1, 10)) + ' разів на тиждень')
#     answered_question = True
elif re.search(fr"\b{keyword}\b.*\bскільки\b.*\bразів\b.*\bтиждень\b", text, re.IGNORECASE) and not answered_question:
    bot.send_message(message.chat.id, 'Десь ' + str(random.randint(1, 10)) + ' разів на тиждень')
    answered_question = True
# elif text.startswith(f"{keyword} ") and writeRandom in text:
#     bot.send_message(message.chat.id, 'Моє рандомне число, це: ' + str(random.randint(1, 1000)))
elif text.startswith(f"{keyword} ") and '?' in text:
    bot.send_message(message.chat.id, random.choice(['Так', 'Ні']))
# else:
#     bot.send_message(message.chat.id, "Я не розумію тебе")
    

if __name__ == '__main__':
    bot.polling(none_stop=True)