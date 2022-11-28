
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
import requests


response = requests.get('https://studycounts.com/api')
print(response)