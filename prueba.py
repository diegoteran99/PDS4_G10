#https://stackoverflow.com/questions/70022749/telegram-guess-the-number-bot-is-changing-the-secret-number-every-time-it-reci

import random
import telebot
from telebot.types import Message
bot = telebot.TeleBot("5662866930:AAEhXzJuXycvDthZMj4SyP43t__ch6EdqI4")
global on_game
on_game = False
numbers = dict()
users = dict()
wins = dict()

@bot.message_handler(commands=['start'])
def greetings(message):
    bot.send_message(message.chat.id, "/new_number <max_number> <tries> → Starting new number game\n (ex: /new_number 70 3)\n/stats → get all stats of the games")

@bot.message_handler(commands=['new_number'])
def guess_number(message):
    global on_game
    if on_game == False:
        on_game = True
        print("message: ", message.from_user.id)
        print("message.entities: ", message.entities[0].type)
        print("message: ", message.text.split(" ")[1])
        max_number = int(message.text.split(" ")[1])
        global tries
        tries = int(message.text.split(" ")[2])
        bot.send_message(message.chat.id, "Starting new game")
        numbers[message.chat.id] = random.randint(0, max_number)
    else:
        bot.send_message(message.chat.id, "A game is alreday active")

@bot.message_handler(commands=['stats'])
def show_wins(message):
    text = ""
    text += "STATS"
    for a,b in wins.items():
        #text +="\n{} → {} wins".format(a["first_name"]+a["last_name"],a[])
        text +="\n{} → {} wins".format(wins[a]["first_name"]+" "+wins[a]["last_name"],wins[a]["wins"])

    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: True)
def checking(message):
    global on_game
    global tries
    if on_game == True:
        if message.from_user.id not in users:
            users[message.from_user.id] = {
                "first_name": message.from_user.first_name ,
                "last_name": message.from_user.last_name,
                "tries":tries - 1,
                }
        else:
            users[message.from_user.id]["tries"] -= 1

        if message.from_user.id not in wins:
            wins[message.from_user.id] = {
                    "first_name": message.from_user.first_name ,
                    "last_name": message.from_user.last_name,
                    "wins":0}

        try:
            if users[message.from_user.id]["tries"] > 0:
                user_message = int(message.text)
                print("numbers: ", numbers)
                print("message.from_user: ", message.from_user)
                print("user_message: ", user_message)
                print("numbers[message.chat.id]: ", numbers[message.chat.id])
                if user_message > numbers[message.chat.id]:
                    bot.reply_to(message, "your number is greater than mine")
                elif user_message < numbers[message.chat.id]:
                    bot.reply_to(message, "your number is smaller than mine")
                else:
                    bot.reply_to(message, "yep, that's the right number\nThe winner is {}".format(message.from_user.first_name + " " + message.from_user.last_name ))
                    wins[message.from_user.id]["wins"] += 1
                    on_game = False
                    users.clear()
            else:
                bot.reply_to(message, "No more tries available")
        except ValueError:
            bot.send_message(message.chat.id, "you must enter an integer")
        except (TypeError, KeyError):
            bot.send_message(message.chat.id, "there's no number to guess! say /start to st")
        
        print("users: ", users) 
        print("wins: ", wins)
        



bot.infinity_polling()
