import requests
import random
import telebot
from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
bot = telebot.TeleBot("5662866930:AAEhXzJuXycvDthZMj4SyP43t__ch6EdqI4")
global on_game
on_game = False
numbers = dict()
users = dict()
wins = dict()
trivia_first_points = dict()




@bot.message_handler(commands=['new_code'])
def create_code(message):
    global on_game
    if on_game == False:
        on_game = True
        code_length = int(message.text.split(" ")[1])
        global tries
        tries = int(message.text.split(" ")[2])
        bot.send_message(message.chat.id, "Starting new game\n\nEach user has {} tries to guess a secret code with a lenth of {} numbers from 0 to 9 withhout repeating numbers\nUse the /guess_code command before the code you want to try".format(tries, code_length))
        global code_numbers
        code_numbers = []
        while len(code_numbers) != code_length:
            number = random.randint(0, 9)
            if number not in code_numbers:
                code_numbers.append(number)
        global code
        code = ""
        for i in code_numbers:
            code += str(i)
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
            code_numbers = []
            while len(code_numbers) != code_length:
                number = random.randint(0, 9)
                if number not in code_numbers:
                    code_numbers.append(number)
            code = ""
            for i in code_numbers:
                code += str(i)



@bot.message_handler(commands=['guess_code'])
def check_code(message):
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
                user_code = int(message.text.split(" ")[1])
                print("Code we want to guess: ", code)
                correct = 0
                present = 0
                for index,number in enumerate(str(user_code)):
                    if code_numbers[index] == int(number):
                        correct += 1
                    elif int(number) in code_numbers:
                        present += 1
                if correct == len(code_numbers):
                    bot.reply_to(message, "That's the secret code\nThe winner is {}".format(message.from_user.first_name + " " + message.from_user.last_name ))
                    wins[message.from_user.id]["wins"] += 1
                    on_game = False
                    users.clear()
                else:
                    bot.reply_to(message, "You have: \n   {} numbers in the correct position \n   {} numbers that are correct but not in the right position".format(correct, present))

            else:
                alives = False
                for i in users:
                    if users[i]["tries"]!=0:
                        alives = True
                if alives == True:
                    bot.reply_to(message, "No more tries available")
                else:
                    on_game = False
                    bot.send_message(message.chat.id, "Game Over, the secret code was: {}".format(code))

        except ValueError:
            bot.send_message(message.chat.id, "You must enter an integer")
    else:
        bot.send_message(message.chat.id, "There's no code to guess! Create another game")
        

bot.infinity_polling()


"""


print(code_numbers)
print(code) 
correcto = False
intento = input("intenta adivinar el codigo de {} numeros de largo: ".format(largo_codigo))
correctas = 0
presentes = 0
for index,number in enumerate(intento):
    if code_numbers[index] == int(number):
        correctas += 1
    
    elif int(number) in code_numbers:
        presentes += 1
if correctas == largo_codigo:
    print("ganaste")

print("Tienes {} numeros en la posición correcta y {} presentes pero no en su posicion correcta".format(correctas, presentes))
"""