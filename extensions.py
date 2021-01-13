import json
import requests
import config as conf

class CustomException(Exception):
    pass

class ExchangeRates():

    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise CustomException('Одинаковые валюты не имеет смысла конвертировать')
        
        if base not in conf.currency:
            raise CustomException(f'Введенное значение валюты <b>{base}</b> не найдено в справочнике.')

        if quote not in conf.currency:
            raise CustomException(f'Введенное значение валюты <b>{quote}</b> не найдено в справочнике.')

        try:
            amount = float(amount)
        except ValueError:
            raise CustomException(f'Не удалось обработать количество <b>{amount}</b>')
        
        base, quote = conf.currency[base], conf.currency[quote]

        params = {'symbols': base}
        if quote != 'EUR':
            params['base'] = quote

        str_param = ''
        for key, val in params.items():
            str_param = '&'.join((str_param, (key + '=' + val)))
        
        req = requests.get(conf.EXCHURL + '?' + str_param)
        response = json.loads(req.content)
        
        if req.status_code != 200:
            raise CustomException(response['error'])
        
        return response['rates'][base] * amount