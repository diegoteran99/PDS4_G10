#https://stackoverflow.com/questions/70022749/telegram-guess-the-number-bot-is-changing-the-secret-number-every-time-it-reci

import random
import telebot

bot = telebot.TeleBot("5662866930:AAEhXzJuXycvDthZMj4SyP43t__ch6EdqI4", parse_mode=None)


numbers = dict()

@bot.message_handler(commands=('start'))
def guess_number(message):
    numbers[message.chat.id] = random.randint(0, 100)

@bot.message_handler(func=lambda message: True)
def checking(message):
    try:
        user_message = int(message.text)
        if user_message > numbers[message.chat.id]:
            bot.send_message(message.chat.id, "your number is greater than mine")
        elif user_message < numbers[message.chat.id]:
            bot.send_message(message.chat.id, "your number is smaller than mine")
        else:
            bot.send_message(message.chat.id, "yep, that's the right number")
    except ValueError:
        bot.send_message(message.chat.id, "you must enter an integer")
    except (TypeError, KeyError):
        bot.send_message(message.chat.id, "there's no number to guess! say /start to start")