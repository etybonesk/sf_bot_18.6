import telebot  # подключаем телегу
import datetime  # для текущей даты
from config import keys, TOKEN  # получаем валюты и токен
from extensions import ConvertionException, CryptoConverter, AmountNum


bot = telebot.TeleBot(TOKEN)  # подключаемся к боту


@bot.message_handler(commands=['start'])  # обработчик команды /start
def start(message: telebot.types.Message):
    text = 'Добро пожаловать в бот-конвертатор валюты!' \
           '\n\nДля выполнения конвертации введите команду вида:' \
           '\n<исходная валюта> <желаемая валюта> <сумма>' \
           '\n\nТ.е., чтобы узнать цену 1 доллара в рублях, нужно ввести:' \
           '\nдоллар рубль 1' \
           '\n\nДля получения помощи введите /help' \
           '\nДля получения списка доступной валюты введите /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])  # обработчик команды /help
def help(message: telebot.types.Message):
    text = 'Доступные команды:' \
           '\n/start - начать работу с ботом.' \
           '\n/values - список доступной для конвертации валюты.' \
           '\n\nДанные о курсах получены с CryptoCompare.com.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])  # обработчик команды /values
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():  # берем значения ключей и выводим по одному на строку
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])  # главный обработчик
def convert(message: telebot.types.Message):
    today = datetime.datetime.now()  # получение текущей даты
    current_date = today.strftime('%H:%M %d-%m-%Y')  # задание текущей даты в нужном формате
    try:
        values = message.text.split(' ')  # парсинг ввода пользователя

        if len(values) != 3:  # сообщение пользователю если много/мало параметров
            raise ConvertionException('Неверное количество параметров.')

        quote, base, amount = values  # задание переменных из запроса для получения данных
        quote, base = quote.lower(), base.lower()  # перевод валюты в нижний индекс, чтобы не было ошибки ввода
        # при верном запросе с заглавными буквами
        amount = amount.replace(',', '.')  # замена запятой на точку, чтобы не было ошибки ввода

        total_base = CryptoConverter.get_price(quote, base, amount)  # обработка запроса

        f_quote = AmountNum.amount_num(float(amount), quote)  # получение валюты в подходящем склонении
        f_base = AmountNum.amount_num(float(total_base), base)  # получение валюты в подходящем склонении
    except ConvertionException as e:  # вывод ошибки, если косяк ввода пользователя
        bot.reply_to(message, f'Неверный ввод:\n{e}')
    except Exception as e:  # вывод ошибки, если косяк системы
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}'
                              f'Мы уже работаем над этой проблемой!')
    else:  # вывод ответа на запрос пользователя
        text = f'На {current_date}:\n' \
               f'{abs(float(amount))} {f_quote} стоит {abs(float(total_base))} {f_base}.'  # цифровые значения взяты по
        # модулю, чтобы не выдавать отрицательные значения в ответе, результат все равно не изменится
        bot.send_message(message.chat.id, text)


bot.polling()
