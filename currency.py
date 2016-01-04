import json
import requests

from currencies import currencies

API_KEY = ''


class CurrencyConverter(object):
    API_KEY = API_KEY

    @staticmethod
    def _convert_country_to_currency_code(c_from, c_to):
        currency_codes = []
        countries = [c_from, c_to]
        for country in countries:
            for key, value in currencies.items():
                if country in value:
                    currency_codes.append(key)
        return currency_codes

    @classmethod
    def create_conversion_of_1000(cls, from_country, to_country):
        return cls(from_country, to_country, amount=1000)

    def __init__(self, from_country, to_country, amount):
        self._currency_codes = self._convert_country_to_currency_code(
            c_from=from_country, c_to=to_country)
        self.amount = amount

    def convert(self):
        rate = self.get_conversion_rate()
        return self.amount * rate

    def get_conversion_rate(self):
        url, params = self._create_api_url(CurrencyConverter.API_KEY,
                                           api_type='conversion')
        try:
            rates = json.loads(requests.get(
                url, params=params).content)['rates']
        except KeyError:
            raise ValueError("Must convert from US Dollars")
        rate = self._parse_rates(rates)
        return rate

    def _create_api_url(self, key, api_type=None):
        oxr_url = 'https://openexchangerates.org/api'
        payload = {'app_id': CurrencyConverter.API_KEY,
                   'base': self.currency_codes[0]}
        if api_type:
            oxr_url += '/latest.json'
        return oxr_url, payload

    def _parse_rates(self, rates):
        for key, value in rates.items():
            if str(key) == self.currency_codes[1]:
                return value

    @property
    def currency_codes(self):
        return self._currency_codes
