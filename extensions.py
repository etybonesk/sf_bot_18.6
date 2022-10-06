import math
import requests
import json
from config import keys


class AmountNum:
    @staticmethod
    def amount_num(amount, word):
        a_amount = math.floor(amount)
        b_amount = (2, 3, 4)
        c_amount = (12, 13, 14)
        a_word = ('рубль', 'юань')
        b_word = ('доллар', )

        if word in a_word:
            word = word[0:len(word) - 1]
            if amount % 1 != 0:  # для дробных
                word = word + 'я'
            elif a_amount % 10 == 1 and a_amount % 100 != 11:  # для окончания на 1
                word = word + 'ь'
            elif (a_amount % 10 in b_amount) and (a_amount % 100 not in c_amount):  # для окончания на 2, 3, 4
                word = word + 'я'
            else:
                word = word + 'ей'
            return word
        elif word in b_word:
            if amount % 1 != 0:  # для дробных
                word += 'а'
            elif a_amount % 10 == 1 and a_amount % 100 != 11:  # для окончания на 1
                word = word
            elif (a_amount % 10 in b_amount) and (a_amount % 100 not in c_amount):  # для окончания на 2, 3, 4
                word += 'а'
            else:
                word += 'ов'
            return word
        else:
            return word


class ConvertionException(Exception):  # обработчик для ошибок пользователя
    pass


class CryptoConverter:  # обработчик запросов пользователя
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        try:
            quote_ticker = keys[quote]  # проверка на верный запрос валюты
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}.'
                                      f'\nДля получения списка доступной валюты введите /values.')

        try:
            base_ticker = keys[base]  # проверка на верный запрос валюты
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}.'
                                      f'\nДля получения списка доступной валюты введите /values.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}.')

        if quote == base:  # если валюты в запросе одинаковые
            total_base = amount
        else:
            r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
            # получение валют через CryptoCompare по API
            total_base = json.loads(r.content)[keys[base]] * amount

        return total_base
