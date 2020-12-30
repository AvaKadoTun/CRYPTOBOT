import telebot
from config import  TOKEN, keys
from utils import CryptoConverter, ConvertionException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = 'Чтобы начать работу введите сообщение в следующем формате\n <имя валюты> <валюта в которую хотите перевести> <количество валюты> \n Пользователь может увидеть все валюты введя команду: /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join([text, key])
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values)!=3:
            raise ConvertionException('Слишком много параметров')
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote,base,amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка на стороне сервера {e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base} '
        bot.send_message(message.chat.id, text)



bot.polling()