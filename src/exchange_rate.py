from logger import log
import aiohttp
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

api_url = config['CzechNationalBank']['api_url']

class ExchangeRate:
    def __init__(self):
        self.api_url = api_url

    def fetch_exchange_rate(self):
        # Implement the code to fetch the current CZK/EUR exchange rate
        pass
