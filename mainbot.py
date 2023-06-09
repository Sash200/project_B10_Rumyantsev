import telebot
from extensions import *
from configbot import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text="Привет!\nКакую валюту необходимо конвертировать?\n\nДанные вводятся через пробел.\n" \
         "Пример: USD RUB 100\n(конвертируемая валюта(трехбуквенный код) базовая валюта (трехбуквенный код) количество базовой валюты) \n\n" \
         "Для правильного ввода кода валюты можно посмотреть список доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def echo_test(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key, value in keys2.items():
        text='\n'.join((text, (f'{value} - {key}')))
    bot.reply_to(message, text)
    text = f'Справка: /help'
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values)>3:
            raise APIException('Много введеных параметров')
        elif len(values)<3:
            raise APIException('Мало введеных параметров')

        base, quote, amount = values
        new_price = Converter.convert(quote, base, amount)

    except APIException as e:
        bot.reply_to(message,f'Ошибка ввода параметров, введите заново!\n{e}')

    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')

    else:
        text = f'Стоимость {amount} {base} = {new_price} {quote}'
        bot.send_message(message.chat.id, text)
        text = f'Хотите еще посчитать? Предлагаю посмотреть список конвертируемых валют /values'
    bot.send_message(message.chat.id, text)

bot.polling()
