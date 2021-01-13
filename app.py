import telebot
from extensions import CustomException, ExchangeRates
import config as conf

bot = telebot.TeleBot(conf.TOKEN)

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
        str_ += ', Вас приветствует бот\n\nЯ умею конвертировать валюты\n\n'

    str_ +='Для начала необходимо ввести команду в формате:\n \
<имеющаяся валюта> <нужная валюта> <количество нужной валюты>\n\n \
Введите команду /help для отображения подсказки\n\n \
Введите команду /values, что бы увидеть список доступных валют.'
    
    bot.reply_to(message, str_)

@bot.message_handler(commands=['values'])
def handler_currency(message):
    str_ = 'Список доступных валют:'
    for curr in conf.currency:
        str_ = '\n'.join((str_, curr)) # str_ += '\n' + curr
    bot.reply_to(message, str_)

@bot.message_handler(content_types=['text'])
def handler_text(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        
        if len(values) != 3:
            raise CustomException('Вы ввели неверное количество параметров!')
        
        base, quote, amount = values

        total_amount = ExchangeRates.get_price(base, quote, amount)

    except CustomException as tEx:
        text = f'<b>Внимание!</b>\n{tEx}\n\nДля справки введите команду: /help'
        bot.send_message(message.chat.id, text, parse_mode='HTML')

    except Exception as tEx:
        text = f'<b>Error!</b>\n{tEx}'
        bot.send_message(message.chat.id, text, parse_mode='HTML')
    
    else:
        result = f'для покупки {amount}{conf.currency[quote]} вам понадобится {str(total_amount)}{conf.currency[base]}'
        bot.send_message(message.chat.id, result)

bot.polling(none_stop = True)