from logger import log
import aiohttp
import asyncio
import json
import configparser
from logger import log
from datetime import date, datetime, timedelta

config = configparser.ConfigParser()
config.read('config.ini')

api_url = config['CzechNationalBank']['api_url']

class ExchangeRate:
    def __init__(self):
        self.api_url = api_url
        self.url = "https://api.example.com/ote-cr-api/v1/hourly_spot_prices"
        self.spot_electricity_price_today = [0.0] * 24
        self.spot_electricity_price_today_valid = True # TODO must be invalidated at midnight
        self.spot_electricity_price_last_update_time = None
        my_array = [0.0] * 24

    async def async_update_exchange_rate(self):
        
        log.info("Fetching daily EUR/CZK exchange rate from CNB...")

        today_date_local = date.today()
        timestamp_now = datetime.now()

        # today_date is formatted as string in format DD.MM.YYYY for get request
        today_date = today_date_local.strftime("%d.%m.%Y")

        exchange_rate = None

        try:
            async with aiohttp.ClientSession() as session:
                request_time = datetime.now()
                # download today and yesterday rates
                # https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date=12.11.2020
                async with session.get(f'https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date={today_date}') as resp:
                    log.debug(f'get: {resp.status}')
                    #print(resp.status)
                    #print(await resp.text())

                    log.debug(f'CNB exchange rate response: "{resp}"')
                    result = await resp.text()
                    request_duration = datetime.now() - request_time
                    log.debug(f'CNB exchange rate request duration: "{request_duration}"')
                    log.debug(f'CNB exchange rate result: "{result}"')

                    # parse result
                    currencies = result.splitlines()
                    # log.info(f'EnergyRouting: currencies: "{currencies}"')
                    # 1. line: "24.02.2023 #40"
                    # 2. line: "země|měna|množství|kód|kurz"
                    # 3. line: "Austrálie|dolar|1|AUD|15,100"
                    # ...
                    if len(currencies) >= 2:

                        rate_date = currencies[0].split(" #")[0]
                        log.info(f'CNB exchange rate EUR/CZK rate date: "{rate_date}"')

                        for currency in currencies[2:]:
                            log.debug(f'CNB exchange rate currency: "{currency}"')
                            if currency == "": # skip empty lines
                                continue
                            currency_data = currency.split("|")
                            log.debug(f'CNB exchange rate currency_data: "{currency_data}"')
                            if len(currency_data) == 5 and currency_data[3] == "EUR":
                                exchange_rate = float(currency_data[4].replace(",", "."))
                                log.info(f'CNB exchange rate received daily EUR/CZK exchange rate from CNB: {exchange_rate} CZK/EUR')
                                break
                    else:
                        log.error(f'CNB exchange rate error parsing EUR/CZK rate from CNB: unexpected response: "{result}"')
                        return None
                    
                    return exchange_rate
               
        except OSError as err:
            log.error(f'CNB exchange rate error receiving EUR/CZK rate from CNB: "{err}"')
            self.today_rate_valid = False
            self.previous_rate_valid = False
