#https://stackoverflow.com/questions/70022749/telegram-guess-the-number-bot-is-changing-the-secret-number-every-time-it-reci

import random
import telebot
from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
bot = telebot.TeleBot("5662866930:AAEhXzJuXycvDthZMj4SyP43t__ch6EdqI4")
global on_game
on_game = False
numbers = dict()
users = dict()
wins = dict()
import requests


base_url = "https://the-trivia-api.com/"



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
        alives = False
        for i in users:
            if users[i]["tries"]!=0:
                alives = True
        if alives == True:
            bot.send_message(message.chat.id, "A game is alreday active")
        else:
            on_game = True
            max_number = int(message.text.split(" ")[1])
            tries = int(message.text.split(" ")[2])
            bot.send_message(message.chat.id, "Starting new game\n\nEach user has {} tries to guess a secret number from 0 to {}\nUse the /number command before the number you want to try".format(tries, max_number))
            numbers[message.chat.id] = random.randint(0, max_number)

@bot.message_handler(commands=['stats'])
def show_wins(message):
    text = ""
    text += "STATS"
    for a in wins.keys():
        text +="\n{} → {} wins".format(wins[a]["first_name"]+" "+wins[a]["last_name"],wins[a]["wins"])
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['trivia_first'])
def create_game(message):
    print("create_game")
    global markup
    markup = ReplyKeyboardRemove()
    global cant_preguntas
    cant_preguntas = message.text.split(" ")[1]
    response = requests.get('{}/api/questions?limit={}'.format(base_url, cant_preguntas))
    global data
    data = response.json()
    global current_question
    current_question = 0
    markup = ReplyKeyboardMarkup(
        one_time_keyboard=True, 
        row_width = 1, 
        resize_keyboard=True)
    
    markup.add("Play")
    msg = bot.send_message(message.chat.id, "Game started, total questions: {}\nSay \"Play\" to start the game".format(cant_preguntas),reply_markup=markup )
    bot.register_next_step_handler(msg, play_game)

def play_game(message):
    global markup
    markup = ReplyKeyboardRemove()
    if int(current_question) != int(cant_preguntas):
        if message.text == "Play" or message.text == "Next":
            print("playgame")
            print("current_question: ",current_question)
            print("correcct answer: ",data[current_question]["correctAnswer"])
            alternativas = []
            alternativas.append(data[current_question]["correctAnswer"])
            for i in data[current_question]["incorrectAnswers"]:
                alternativas.append(i)

            random.shuffle(alternativas)
            markup = ReplyKeyboardMarkup(
                one_time_keyboard=True, 
                row_width = 1, 
                input_field_placeholder="Select your answer", 
                resize_keyboard=True)
            
            markup.add(alternativas[0], alternativas[1], alternativas[2], alternativas[3])
            msg = bot.send_message(message.chat.id, data[current_question]["question"], reply_markup=markup )
            bot.register_next_step_handler(msg, check_answer)
        else:
            msg = bot.send_message(message.chat.id, "Wrong option")
            bot.register_next_step_handler(msg, play_game)
    else:
        bot.send_message(message.chat.id, "The game has ended, the winner is ...")
        #decir que termino y mostrar el ganador 
    

def check_answer(message):
    print("check_answer")
    global current_question
    global markup
    print("message.text: ", message.text)
    print("data[current_question][correctAnswer]: ", data[current_question]["correctAnswer"])
    if message.text == data[current_question]["correctAnswer"]:
        bot.reply_to(message, "Thats the right answer")
        current_question += 1
        markup = ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            row_width = 1, 
            resize_keyboard=False)
        
        markup.add("Next")
        msg = bot.send_message(message.chat.id, "Ready for next question?",reply_markup=markup )
        bot.register_next_step_handler(msg, play_game)
    else:
        msg = bot.send_message(message.chat.id, "Thats not the right answer, keep trying!",reply_markup=markup )
        bot.register_next_step_handler(msg, check_answer)

    
    
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
                print("Number we want to guess: ", numbers[message.chat.id])
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