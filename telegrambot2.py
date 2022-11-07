#https://api.telegram.org/bot5662866930:AAEhXzJuXycvDthZMj4SyP43t__ch6EdqI4/getUpdates
#https://api.telegram.org/bot5662866930:AAEhXzJuXycvDthZMj4SyP43t__ch6EdqI4/sendMessage?text=hifromBot&chat_id=5633096037
#https://www.youtube.com/watch?v=VcwuWzFcjQI

from calendar import day_abbr
from time import time
token = '5662866930:AAEhXzJuXycvDthZMj4SyP43t__ch6EdqI4'

import requests
import datetime
import json
import time
import urllib
import random

TOKEN = token
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_json_from_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    js = json.loads(content)
    return js

def get_telegram_update(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def echo_all(updates):
    for update in updates["result"]:
        last_chat_text = (update["message"]["text"])
        last_chat_name = update['message']['chat']['first_name']
        last_chat_id = update['message']['chat']['id']
        greetings = ('hello', 'hi', 'greetings', 'sup')
        now = datetime.datetime.now()
        new_offset = None
        today = now.day
        hour = now.hour
        print(last_chat_text)
        print(last_chat_name)
        if last_chat_text.lower().startswith("/new_number"):
                max_number = int(last_chat_text.lower().split(" ")[1])
                tries = int(last_chat_text.lower().split(" ")[2])
                random_number = random.randint(0, max_number)
                text = 'Una partida de number ha sido creada\n - numero mayor: {}\n - numero de intentos por persona: {}'.format(max_number, tries)
                send_telegram_message(text, last_chat_id)
 
        if last_chat_text.lower().startswith("/number"):
                trying_number = int(last_chat_text.lower().split(" ")[1])
                if trying_number == random_number:
                    text = 'Correcto!'
                    send_telegram_message(text, last_chat_id)
                else:
                    if trying_number > random_number:
                        text = 'El número es menor'
                        send_telegram_message(text, last_chat_id)
                    else:
                        text = 'El número es mayor'
                        send_telegram_message(text, last_chat_id)


        text = "this is a telegram bot - replying back to your message: " + update["message"]["text"]
        print(text)
        chat = update['message']['chat']['id']
        print(chat)
        send_telegram_message(text, chat)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]['message']['chat']['id']
    return (text, chat_id)

def send_telegram_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    response = requests.get(url)
    content = response.content.decode("utf8")

def main():
    last_update_id = None
    print(URL)

    while True:
        updates = get_telegram_update(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
    time.sleep(0.5)

greetings = ('hello', 'hi', 'greetings', 'sup')
now = datetime.datetime.now()

if __name__ == '__main__':
    main()