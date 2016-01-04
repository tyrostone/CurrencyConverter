import json
import requests

from currencies import currencies

API_KEY = ''


class CurrencyConverter(object):
    """CurrencyConverter

       An object that converts currencies

    """
    API_KEY = API_KEY

    @staticmethod
    def _maybe_get_rates(url, params):
        """_maybe_get_rates

            Attempts to get rates from Open Exchange Rates
            If the API key is not a paid subscription,
            user will only receive rates if converting from USD

        :param url:
            URL to be processed via requests
        :param params:
            params to include in request (e.g. API key)
        """
        try:
            rates = json.loads(requests.get(
                url, params=params).content)['rates']
        except KeyError:
            raise ValueError("Must convert from US Dollars")
        return rates

    @staticmethod
    def _convert_country_to_currency_code(c_from, c_to):
        """_convert_country_to_currency_code

            Converts country names to currency codes

        :param c_from:
            Country to convert currency from (str)
        :param c_to:
            Country to convert currency to (str)
        """
        currency_codes = []
        countries = [c_from, c_to]
        for country in countries:
            for key, value in currencies.items():
                if country in value:
                    currency_codes.append(key)
        return currency_codes

    @classmethod
    def create_conversion_of_1000(cls, from_country, to_country):
        """create_conversion_of_1000

           Creates a CurrencyConverter object with an amount value of 1000

        """
        return cls(from_country, to_country, amount=1000)

    def __init__(self, from_country, to_country, amount):
        """__init__

            Creates a CurrencyConverter object

        :param from_country:
            Country to convert currency from (str)
        :param to_country:
            Country to convert currency to (str)
        :param amount:
            Amount to convert
        """
        self._currency_codes = self._convert_country_to_currency_code(
            c_from=from_country, c_to=to_country)
        self.amount = amount

    def convert(self):
        """convert

            Performs currency conversion

        """
        rate = self.get_conversion_rate()
        return self.amount * rate

    def get_conversion_rate(self):
        """get_conversion_rate

            Generates URL and parameters to query the Open Exchange Rates API
            Queries the API, which possibly returns rates, finds approprate
            conversion rate

        """
        url, params = self._create_api_url(CurrencyConverter.API_KEY,
                                           api_type='conversion')
        print url, params
        rates = self._maybe_get_rates(url, params)
        rate = self._parse_rates(rates)
        return rate

    def _create_api_url(self, key, api_url=None):
        """_create_api_url

        :param key:
            API key to use in URL
        :param api_url:
            Specific URL to be received from API
        """
        oxr_url = 'https://openexchangerates.org/api'
        payload = {'app_id': CurrencyConverter.API_KEY,
                   'base': self.currency_codes[0]}
        if api_url:
            oxr_url += '/latest.json'
        return oxr_url, payload

    def _parse_rates(self, rates):
        for key, value in rates.items():
            if str(key) == self.currency_codes[1]:
                return value

    @property
    def currency_codes(self):
        return self._currency_codes
