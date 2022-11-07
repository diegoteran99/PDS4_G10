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

@bot.message_handler(commands=['start', 'help', 'greetings'])
def greetings(message):
    bot.send_message(message.chat.id, "COMMANDS\n\n- /new_number <max_number> <tries> → Start a new number game (ex: /new_number 70 3)\n\n- /stats → Get all the wins of the users\n\n- /number <number>→ Select the number that you want to use (ex: /number 14)")

@bot.message_handler(commands=['new_number'])
def guess_number(message):
    global on_game
    if on_game == False:
        on_game = True
        max_number = int(message.text.split(" ")[1])
        global tries
        tries = int(message.text.split(" ")[2])
        bot.send_message(message.chat.id, "Starting new game\n\nEach user has {} tries to guess a secret number from 0 to {}\nUse the /number command before the number you want to try".format(tries, max_number))
        numbers[message.chat.id] = random.randint(0, max_number)
    else:
        bot.send_message(message.chat.id, "A game is alreday active")

@bot.message_handler(commands=['stats'])
def show_wins(message):
    text = ""
    text += "STATS"
    for a in wins.keys():
        text +="\n{} → {} wins".format(wins[a]["first_name"]+" "+wins[a]["last_name"],wins[a]["wins"])
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['number'])
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
                user_message = int(message.text.split(" ")[1])
                #print("Number we want to guess: ", numbers[message.chat.id])
                if user_message > numbers[message.chat.id]:
                    bot.reply_to(message, "That number is greater than the secret number\nYou have {} tries left".format(users[message.from_user.id]["tries"]))
                elif user_message < numbers[message.chat.id]:
                    bot.reply_to(message, "That number is smaller than the secret number\nYou have {} tries left".format(users[message.from_user.id]["tries"]))
                else:
                    bot.reply_to(message, "That's the secret number\nThe winner is {}".format(message.from_user.first_name + " " + message.from_user.last_name ))
                    wins[message.from_user.id]["wins"] += 1
                    on_game = False
                    users.clear()
            else:
                bot.reply_to(message, "No more tries available")
        except ValueError:
            bot.send_message(message.chat.id, "You must enter an integer")
        except (TypeError, KeyError):
            bot.send_message(message.chat.id, "There's no number to guess! Create another game")
        
bot.infinity_polling()
