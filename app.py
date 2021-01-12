import telebot
import json
import requests
from config import currency, TOKEN

bot = telebot.TeleBot(TOKEN)

class CustomException(Exception):
    pass

class ExchangeRates():
    pass

@bot.message_handler(commands=['start','help'])
def handler_start_help(message: telebot.types.Message):
    str_ = ''
    if message.text == '/start':        
        if message.chat.username != None and isinstance(message.chat.username, str):
            str_ = message.chat.username
        else:
            if message.chat.first_name != None and isinstance(message.chat.first_name, str): 
                str_ = message.chat.first_name
            if message.chat.last_name and isinstance(message.chat.last_name, str):
                str_ += ' ' + message.chat.last_name
        str_ += ', Вас приветствует бот\n\n'

    str_ +='Я умею конвертировать валюты\n\nДля начала необходимо ввести команду в формате:\n \
<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n\nНаберите команду /currency, что бы увидеть список доступных валют.'
    
    bot.reply_to(message, str_)

@bot.message_handler(commands=['currency'])
def handler_currency(message):
    str_ = 'Список доступных валют:'
    for curr in currency:
        str_ = '\n'.join((str_, curr)) # str_ += '\n' + curr
    bot.reply_to(message, str_)

bot.polling(none_stop = True)