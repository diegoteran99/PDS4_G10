import requests
import time 
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
trivia_time_points = dict()


global initial_time
global current_time

base_url = "https://the-trivia-api.com/"

@bot.message_handler(commands=['start', 'help', 'greetings', 'commands'])
def greetings(message):
    bot.send_message(message.chat.id, "COMMANDS\n\n- /stats → Get all the wins of the users\n\n- /new_number <max_number> <tries> → Start a new number game \n(ex: /new_number 70 3)\n\n- /number <number>→ Select the number that you want to use \n(ex: /number 14)\n\n- /trivia_first <number of questions>→Start a trivia game in \"first\" mode\n(ex: /trivia_first 5)\n\n- /trivia_time <number of questions> <seconds to answer>→ Start a trivia game in \"time\" mode\n(ex: /trivia_time 4 15)\n\n- /new_code <code_length> <tries>→ Start a game where you have to guess a code of maximum 5 numbers from 0 to 5 where with every atempt you see if a number is correct or not and if is in the correct position.\n(ex: /new_code 7 3)\n\n- /guess_code <code>→ Select a code that you want to try with\n(ex: /guess_code 1357986)")


@bot.message_handler(commands=['new_number'])
def guess_number(message):
    global on_game
    if len(message.text.split(" ")) == 3:
        if on_game == False:
            on_game = True
            global max_number
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
    else:
        bot.reply_to(message, "The comand is not correct.\nIt has to be with the form /new_number <max_number> <tries>")


@bot.message_handler(commands=['number'])
def checking(message):
    valid_number = True
    if int(message.text.split(" ")[1]) < 0 or int(message.text.split(" ")[1]) > max_number:
            valid_number = False
    if valid_number and len(message.text.split(" ")) == 2:
        global on_game
        global tries
        if on_game == True:
            if message.from_user.id not in users:
                users[message.from_user.id] = {
                    "first_name": message.from_user.first_name ,
                    "last_name": message.from_user.last_name,
                    "tries":tries,
                    }
            

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
                        users[message.from_user.id]["tries"] -= 1
                        bot.reply_to(message, "That number is greater than the secret number\nYou have {} tries left".format(users[message.from_user.id]["tries"]))
                    elif user_message < numbers[message.chat.id]:
                        users[message.from_user.id]["tries"] -= 1
                        bot.reply_to(message, "That number is smaller than the secret number\nYou have {} tries left".format(users[message.from_user.id]["tries"]))
                    else:
                        bot.reply_to(message, "That's the secret number\nThe winner is {}".format(message.from_user.first_name + " " + message.from_user.last_name ))
                        wins[message.from_user.id]["wins"] += 1
                        on_game = False
                        users.clear()
                    if users[message.from_user.id]["tries"] <= 0:
                        alives = False
                        for i in users:
                            if users[i]["tries"]>0:
                                alives = True
                        if alives == True:
                            bot.reply_to(message, "No more tries available")
                        else:
                            bot.send_message(message.chat.id, "Game Over, the secret number was: {}".format(numbers[message.chat.id]))
                            on_game = False
                            users.clear()
            except ValueError:
                bot.send_message(message.chat.id, "You must enter an integer")
            except (TypeError, KeyError):
                bot.send_message(message.chat.id, "There's no number to guess! Create another game")
        else:    
            bot.send_message(message.chat.id, "There's no number to guess! Create another game")
    else:
        bot.reply_to(message, "The comand is not correct.\nIt has to be with the form /number <number>")
        

@bot.message_handler(commands=['stats'])
def show_wins(message):
    text = ""
    text += "STATS"
    for a in wins.keys():
        text +="\n{} → {} wins".format(wins[a]["first_name"]+" "+wins[a]["last_name"],wins[a]["wins"])
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['trivia_first'])
def create_game(message):
    if len(message.text.split(" ")) == 2:

        if on_game == False:
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
            
            markup.add("/Play")
            msg = bot.send_message(message.chat.id, "Game started, total questions: {}\nSay \"Play\" to start the game".format(cant_preguntas),reply_markup=markup )
            bot.register_next_step_handler(msg, play_game)
        else:
            bot.send_message(message.chat.id, "A game is already active, finish that one first")
    else:
        bot.reply_to(message, "The comand is not correct.\nIt has to be with the form /trivia_first <number of questions>")

def play_game(message):
    global markup
    global on_game
    markup = ReplyKeyboardRemove()
    if int(current_question) != int(cant_preguntas):
        if message.text == "/Play" or message.text == "/Next":
            print("correcct answer: ",data[current_question]["correctAnswer"])
            global alternativas
            alternativas = []
            alternativas.append(data[current_question]["correctAnswer"])
            for i in data[current_question]["incorrectAnswers"]:
                alternativas.append(i)

            random.shuffle(alternativas)
            markup = ReplyKeyboardMarkup(
                one_time_keyboard=True, 
                row_width = 2, 
                input_field_placeholder="Select your answer", 
                resize_keyboard=False)
            
            markup.add("A)","B)","C)","D)")
            msg = bot.send_message(message.chat.id,

            "QUESTION {}/{}\n{}\n\nA) {}\nB) {}\nC) {}\nD) {}\n".format(current_question+1,cant_preguntas,data[current_question]["question"],alternativas[0], alternativas[1], alternativas[2], alternativas[3])
            
            , reply_markup=markup )
            bot.register_next_step_handler(msg, check_answer)
        else:
            msg = bot.send_message(message.chat.id, "Wrong option")
            bot.register_next_step_handler(msg, play_game)
        
    else:
        winners = []
        highest_value = 0
        for user_id in trivia_first_points:
            if trivia_first_points[user_id]["points"] > highest_value:
                winners = [user_id]
                highest_value = trivia_first_points[user_id]["points"]

            elif trivia_first_points[user_id]["points"] == highest_value:
                winners.append(user_id)
        
        if len(winners) > 1:
            text = "The winners are:\n\n"
            for i in winners:
                text+="{}\n".format(trivia_first_points[i]["first_name"]+ " "+trivia_first_points[i]["last_name"])
            text+="\nWith a total of {} points".format(trivia_first_points[winners[0]]["points"])
        else:
            text = "The winners is:\n\n{}\n\nWith a total of {} points".format(trivia_first_points[winners[0]]["first_name"]+ " "+trivia_first_points[winners[0]]["last_name"],trivia_first_points[winners[0]]["points"])
        bot.send_message(message.chat.id, text)
        trivia_first_points.clear()
        for i in winners: 
            wins[i]["wins"] += 1
        on_game = False

def check_answer(message):
    if message.from_user.id not in trivia_first_points:
        trivia_first_points[message.from_user.id] = {
                "first_name": message.from_user.first_name ,
                "last_name": message.from_user.last_name,
                "points":0}
    if message.from_user.id not in wins:
            wins[message.from_user.id] = {
                    "first_name": message.from_user.first_name ,
                    "last_name": message.from_user.last_name,
                    "wins":0}

    global current_question
    global markup
    global alternativas
    if message.text == "A)":
        answer = alternativas[0]
    elif message.text == "B)":
        answer = alternativas[1]
    elif message.text == "C)":
        answer = alternativas[2]
    elif message.text == "D)":
        answer = alternativas[3]

    if answer == data[current_question]["correctAnswer"]:
        bot.reply_to(message, "Thats the right answer")
        current_question += 1
     
        trivia_first_points[message.from_user.id]["first_name"] = message.from_user.first_name
        trivia_first_points[message.from_user.id]["last_name"] = message.from_user.last_name
        trivia_first_points[message.from_user.id]["points"] += 1

        markup = ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            row_width = 1, 
            resize_keyboard=True)
        text = ""
        for i in trivia_first_points:
            text+="{} → {} points\n".format(trivia_first_points[i]["first_name"]+ " "+trivia_first_points[i]["last_name"],trivia_first_points[i]["points"])
        bot.send_message(message.chat.id, text)
            
        if int(current_question) != int(cant_preguntas):
            markup.add("/Next")
            msg = bot.send_message(message.chat.id, "Ready for next question?",reply_markup=markup )
            bot.register_next_step_handler(msg, play_game)
        else:
            markup.add("/End Game")
            msg = bot.send_message(message.chat.id, "No more questions left",reply_markup=markup )
            bot.register_next_step_handler(msg, play_game)
    else:
        msg = bot.send_message(message.chat.id, "Thats not the right answer, keep trying!",reply_markup=markup )
        bot.register_next_step_handler(msg, check_answer)


@bot.message_handler(commands=['new_code'])
def create_code(message):
    if len(message.text.split(" ")) == 3 and int(message.text.split(" ")[1]) <= 5:
        global on_game
        if on_game == False:
            on_game = True
            code_length = int(message.text.split(" ")[1])
            global tries
            tries = int(message.text.split(" ")[2])
            bot.send_message(message.chat.id, "Starting new game\n\nEach user has {} tries to guess a secret code with a length of {} numbers from 0 to 5 withhout repeating numbers\nUse the /guess_code command before the code you want to try".format(tries, code_length))
            global code_numbers
            code_numbers = []
            while len(code_numbers) != code_length:
                number = random.randint(0, 5)
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
    else:
        bot.reply_to(message, "The comand is not correct.\nIt has to be with the form /new_code <code_length> <tries>")


@bot.message_handler(commands=['guess_code'])
def check_code(message):
    valid_code = True
    for i in message.text.split(" ")[1]:
        if int(i) < 0 and int(i) > 5:
            valid_code = False
        if message.text.split(" ")[1].count(i) > 1:
            valid_code = False
    if valid_code and len(message.text.split(" ")) == 2 :
        global on_game
        global tries
        global code
        if on_game == True:
            if message.from_user.id not in users:
                users[message.from_user.id] = {
                    "first_name": message.from_user.first_name ,
                    "last_name": message.from_user.last_name,
                    "tries":tries,
                    }

            if message.from_user.id not in wins:
                wins[message.from_user.id] = {
                        "first_name": message.from_user.first_name ,
                        "last_name": message.from_user.last_name,
                        "wins":0}
            
            try:
                user_code = int(message.text.split(" ")[1])
                print("Code we want to guess: ", code)
                correct = 0
                present = 0
                for index,number in enumerate(str(user_code)):
                    if code_numbers[index] == int(number):
                        correct += 1
                    elif int(number) in code_numbers:
                        present += 1
                if users[message.from_user.id]["tries"] > 0:        
                    if correct != len(code_numbers):
                        users[message.from_user.id]["tries"] -= 1
                        bot.reply_to(message, "You have: \n   {} numbers in the correct position \n   {} numbers that are correct but not in the right position\nYou have {} tries left".format(correct, present, users[message.from_user.id]["tries"]))
                        
                    else:
                        bot.reply_to(message, "That's the secret code\nThe winner is {}".format(message.from_user.first_name + " " + message.from_user.last_name ))
                        wins[message.from_user.id]["wins"] += 1
                        on_game = False
                        users.clear()
                    

                    if users[message.from_user.id]["tries"] <= 0:
                        alives = False
                        for i in users:
                            if users[i]["tries"]!=0:
                                alives = True
                        if alives == True:
                            bot.reply_to(message, "No more tries available")
                        else:
                            user_code = int(message.text.split(" ")[1])
                            correct = 0
                            present = 0
                            for index,number in enumerate(str(user_code)):
                                if code_numbers[index] == int(number):
                                    correct += 1
                                elif int(number) in code_numbers:
                                    present += 1
                            on_game = False
                            bot.reply_to(message, "You have: \n   {} numbers in the correct position \n   {} numbers that are correct but not in the right position".format(correct, present))
                            bot.send_message(message.chat.id, "Game Over, the secret code was: {}".format(code))
                            users.clear()
            except ValueError:
                bot.send_message(message.chat.id, "You must enter an integer")
            except (TypeError, KeyError):
                bot.send_message(message.chat.id, "There's no code to guess! Create another game")
        else:
            bot.send_message(message.chat.id, "There's no code to guess! Create another game")
    else:
        bot.reply_to(message, "The comand is not correct.\nIt has to be with the form /guess_code <code> and numbers between 0 and 5")


@bot.message_handler(commands=['trivia_time'])
def create_game_time(message):
    if len(message.text.split(" ")) == 3:
        if on_game == False:
            global markup
            markup = ReplyKeyboardRemove()
            global cant_preguntas
            global tiempo_juego
            cant_preguntas = message.text.split(" ")[1]
            tiempo_juego = message.text.split(" ")[2]
            response = requests.get('{}/api/questions?limit={}'.format(base_url, cant_preguntas))
            global data
            data = response.json()
            global current_question
            current_question = 0
            markup = ReplyKeyboardMarkup(
                one_time_keyboard=True, 
                row_width = 1, 
                resize_keyboard=True)
            
            markup.add("/Play")
            msg = bot.send_message(message.chat.id, "Game started, total questions: {}\nSay \"Play\" to start the game".format(cant_preguntas),reply_markup=markup )
            bot.register_next_step_handler(msg, play_game_time)
        else:
            bot.send_message(message.chat.id, "A game is already active, finish that one first")
    else:
        bot.reply_to(message, "The comand is not correct.\nIt has to be with the form /trivia_time <number of questions> <seconds to answer>")

def play_game_time(message):
    global markup
    global on_game
    global initial_time

    markup = ReplyKeyboardRemove()
    if int(current_question) != int(cant_preguntas):
        if message.text == "/Play" or message.text == "/Next":
            print("correcct answer: ",data[current_question]["correctAnswer"])
            initial_time = time.time()
            global alternativas
            alternativas = []
            alternativas.append(data[current_question]["correctAnswer"])
            for i in data[current_question]["incorrectAnswers"]:
                alternativas.append(i)

            random.shuffle(alternativas)
            markup = ReplyKeyboardMarkup(
                one_time_keyboard=True, 
                row_width = 2, 
                input_field_placeholder="Select your answer", 
                resize_keyboard=False)
            
            markup.add("A)","B)","C)","D)")

            msg = bot.send_message(message.chat.id,

            "QUESTION {}/{}\n{}\n\nA) {}\nB) {}\nC) {}\nD) {}\n".format(current_question+1,cant_preguntas,data[current_question]["question"],alternativas[0], alternativas[1], alternativas[2], alternativas[3])
            
            , reply_markup=markup )

            
            bot.register_next_step_handler(msg, check_answer_time)
            
        else:
            msg = bot.send_message(message.chat.id, "Wrong option")
            bot.register_next_step_handler(msg, play_game_time)
    else:
        winners = []
        highest_value = 0
        for user_id in trivia_time_points:
            if trivia_time_points[user_id]["points"] > highest_value:
                winners = [user_id]
                highest_value = trivia_time_points[user_id]["points"]

            elif trivia_time_points[user_id]["points"] == highest_value:
                winners.append(user_id)
        
        if len(winners) > 1:
            text = "The winners are:\n\n"
            for i in winners:
                text+="{}\n".format(trivia_time_points[i]["first_name"]+ " "+trivia_time_points[i]["last_name"])
            text+="\nWith a total of {} points".format(trivia_time_points[winners[0]]["points"])
        else:
            text = "The winners is:\n\n{}\n\nWith a total of {} points".format(trivia_time_points[winners[0]]["first_name"]+ " "+trivia_time_points[winners[0]]["last_name"],trivia_time_points[winners[0]]["points"])
        bot.send_message(message.chat.id, text)
        trivia_time_points.clear()
        for i in winners: 
            wins[i]["wins"] += 1
        on_game = False

def check_answer_time(message):
    global markup
    global current_question
    current_time = time.time()
    print("current_time: ", current_time)
    print("time_passed: ", round(current_time - initial_time,1))
    print("correcct answer: ",data[current_question]["correctAnswer"])
    if message.from_user.id not in trivia_time_points:
            trivia_time_points[message.from_user.id] = {
                    "first_name": message.from_user.first_name ,
                    "last_name": message.from_user.last_name,
                    "points":0}
    if message.from_user.id not in wins:
            wins[message.from_user.id] = {
                    "first_name": message.from_user.first_name ,
                    "last_name": message.from_user.last_name,
                    "wins":0}

    if current_time - initial_time < float(tiempo_juego):
        global alternativas
        if message.text == "A)":
            answer = alternativas[0]
        elif message.text == "B)":
            answer = alternativas[1]
        elif message.text == "C)":
            answer = alternativas[2]
        elif message.text == "D)":
            answer = alternativas[3]

        if answer == data[current_question]["correctAnswer"]:
            bot.reply_to(message, "Thats the right answer")
            current_question += 1
        
            trivia_time_points[message.from_user.id]["first_name"] = message.from_user.first_name
            trivia_time_points[message.from_user.id]["last_name"] = message.from_user.last_name
            trivia_time_points[message.from_user.id]["points"] += (round(100/(current_time - initial_time),1))

            markup = ReplyKeyboardRemove()
            markup = ReplyKeyboardMarkup(
                one_time_keyboard=True, 
                row_width = 1, 
                resize_keyboard=True)
            text = ""
            for i in trivia_time_points:
                text+="{} → {} points\n".format(trivia_time_points[i]["first_name"]+ " "+trivia_time_points[i]["last_name"],trivia_time_points[i]["points"])
            bot.send_message(message.chat.id, text)
            if int(current_question) != int(cant_preguntas):
                markup.add("/Next")
                msg = bot.send_message(message.chat.id, "Ready for next question?",reply_markup=markup )
                bot.register_next_step_handler(msg, play_game_time)
            else:
                markup.add("/End Game")
                msg = bot.send_message(message.chat.id, "No more questions left",reply_markup=markup )
                bot.register_next_step_handler(msg, play_game_time)
        else:
            msg = bot.send_message(message.chat.id, "Thats not the right answer, keep trying!",reply_markup=markup )
            bot.register_next_step_handler(msg, check_answer_time)
    else:
        msg = bot.send_message(message.chat.id, "Out of time")
        current_question += 1
        markup = ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            row_width = 1, 
            resize_keyboard=True)
        text = ""
        for i in trivia_time_points:
            text+="{} → {} points\n".format(trivia_time_points[i]["first_name"]+ " "+trivia_time_points[i]["last_name"],trivia_time_points[i]["points"])
        bot.send_message(message.chat.id, text)
            
        if int(current_question) != int(cant_preguntas):
            markup.add("/Next")
            msg = bot.send_message(message.chat.id, "Ready for next question?",reply_markup=markup )
            bot.register_next_step_handler(msg, play_game_time)
        else:
            markup.add("/End Game")
            msg = bot.send_message(message.chat.id, "No more questions left",reply_markup=markup )
            bot.register_next_step_handler(msg, play_game_time)
     
bot.infinity_polling()