import requests
import json
from configbot import keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def convert(quote, base, amount):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты, введите параметры заново"{base}".\nСписок доступных валют: /values')

        try:
            quote_key = keys[quote]
        except KeyError:
            raise APIException(f'"{quote}" такой валюты нет в списке, введите параметры заново\nСписок доступных валют: /values')

        try:
            base_key = keys[base]
        except KeyError:
            raise APIException(f'"{base}" такой валюты нет в списке, введите параметры заново\nСписок доступных валют: /values')

        try:
            amount = float(amount.replace(",", "."))
        except KeyError:
            raise APIException(f'Не удалось обработать количество "{amount}", введите параметры заново')


        headers= {"apikey": "7uImkqZdlPwNiV57yd4YCbyIV4KMsz7Q"}
        r = requests.get( f"https://api.apilayer.com/exchangerates_data/latest?symbols={quote_key}&base={base_key}", headers=headers)
        resp = json.loads(r.content)
        new_price = resp['rates'][quote_key] * amount
        new_price = round(new_price, 2)

        return new_price

