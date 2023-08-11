import aiohttp
import asyncio
import configparser
from logger import log
from datetime import date, datetime, timedelta

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['OTE-CR']['api_key']

class ElectricityPrices:
    def __init__(self):
        self.api_key = api_key
        self.url = "https://api.example.com/ote-cr-api/v1/hourly_spot_prices"
        self.spot_electricity_price_today = [0.0] * 24
        self.spot_electricity_price_today_valid = True # TODO must be invalidated at midnight
        self.spot_electricity_price_last_update_time = None
        my_array = [0.0] * 24
 
    def fetch_prices(self):
        # Implement the code to fetch hourly spot electricity prices from OTE-CR API
        # and return the data in CZK
        pass

    async def async_update_spot_electricity_costs(self):
        log.info("Updating spot electricity costs from OTE-CR")

        today_date_local = date.today()
        timestamp_now = datetime.now()

        try:
            async with aiohttp.ClientSession() as session:
                request_time = datetime.now()
                async with session.get(f'https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data?report_date={today_date_local}') as resp:
                    log.debug(f'get: {resp.status}')
                    #print(resp.status)
                    #print(await resp.text())

                    log.info(f'EnergyRouting: price cost response: "{resp}"')
                    result = await resp.json()
                    request_duration = datetime.now() - request_time
                    log.info(f'EnergyRouting: price cost request duration: "{request_duration}"')
                    log.info(f'EnergyRouting: price cost result: "{result}"')

                    if 'data' in result:
                        if 'dataLine' in result['data']:
                            if len(result['data']['dataLine']) == 2:
                                if 'point' in result['data']['dataLine'][1]:
                                    hourly_spot_price = result['data']['dataLine'][1]['point']
                                    if len(hourly_spot_price) == 24:
                                        for i in range(0, 24):
                                            self.spot_electricity_price_today[i] = hourly_spot_price[i]['y']
                                            self.spot_electricity_price_today_valid = True # TODO must be invalidated at midnight
                                            self.spot_electricity_price_last_update_time = timestamp_now
                                            log.debug(f'EnergyRouting: received daily spot electricity prices from OTE-CR: hour: {i:02d}:00-{(i+1):02d}:00 {self.spot_electricity_price_today[i]} EUR/MWh')
                                        # self.report_hourly_spot_electricity_costs()
                                    else:
                                        log.error(f'EnergyRouting: expected 24 values for daily spot prices, received {len(hourly_spot_price)}')
                                else:
                                    log.error(f'EnergyRouting: missing "point" array in JSON from OTE-CR')
                            else:
                                log.error(f'EnergyRouting: "dataLine" in JSON from OTE-CR does not have expected 2 items - amount and price')
                        else:
                            log.error(f'EnergyRouting: missing "dataLine" array in JSON from OTE-CR')
                    else:
                        log.error(f'EnergyRouting: missing "data" in JSON from OTE-CR')

        except OSError as err:
            log.error(f'EnergyRouting: error receiving data from OTE-CR: "{err}"')

            if timestamp_now - self.spot_electricity_price_last_update_time > timedelta(hours=24):
                self.spot_electricity_price_today_valid = False # invalidate if failed update and last value is depreciated

    async def async_update_czk_eur_exchange_rates(self):
        # download rates from CNB from: https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/graph_data.js?currency=EUR&format=json
        log.info("EnergyRouting: updating daily EUR/CZK exchange rate from CNB")

        today_date_local = date.today()
        # today_date is formatted as string in format YYYY-MM-DD
        #today_date = today_date_local.strftime("%Y-%m-%d")

        # today_date is formatted as string in format DD.MM.YYYY
        today_date = today_date_local.strftime("%d.%m.%Y")

        try:
            # async with self.async_http.get('https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/graph_data.js?currency=EUR&format=json') as resp:
            #     log.info(f'EnergyRouting: exchange rate response: "{resp}"')
            #     result = await resp.json()
            #     log.info(f'EnergyRouting: exchange rate result: "{result}"')

            #     if len(result) > 1:
            #         if result[-1][0] == today_date:
            #             self.today_rate = result[-1][1] # last value is for today
            #             self.today_rate_valid = True
            #             self.previous_rate = result[-2][1] # second last value is for yesterday or last working day
            #             self.previous_rate_valid = True
            #             log.info(f'EnergyRouting: received daily EUR/CZK exchange rate from CNB: {self.today_rate} CZK/EUR')
            #         else:
            #             self.today_rate_valid = False
            #             self.previous_rate = result[-1][1] # last value is for yesterday or last working day
            #             self.previous_rate_valid = True
            #             log.info(f'EnergyRouting: received last valid EUR/CZK exchange rate from CNB: {self.previous_rate} CZK/EUR')
            async with self.async_http.get(f'https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date={today_date}') as resp:
                # log.info(f'EnergyRouting: exchange rate response: "{resp}"')
                result = await resp.text()
                # log.info(f'EnergyRouting: exchange rate result: "{result}"')
                # parse result
                currencies = result.splitlines()
                # log.info(f'EnergyRouting: currencies: "{currencies}"')
                # 1. line: "24.02.2023 #40"
                # 2. line: "země|měna|množství|kód|kurz"
                # 3. line: "Austrálie|dolar|1|AUD|15,100"
                if len(currencies) < 2:
                    log.error(f'EnergyRouting: error receiving EUR/CZK rate from CNB: invalid response')
                    self.today_rate_valid = False
                    self.previous_rate_valid = False
                    return
                rate_date = currencies[0].split(" #")[0]
                log.info(f'EnergyRouting: EUR/CZK rate date: "{rate_date}"')
                self.today_rate_valid = False

                for currency in currencies[2:]:
                    # log.info(f'EnergyRouting: currency: "{currency}"')
                    if currency == "": # skip empty lines
                        continue
                    currency_data = currency.split("|")
                    # log.info(f'EnergyRouting: currency_data: "{currency_data}"')
                    if len(currency_data) == 5 and currency_data[3] == "EUR":
                        if rate_date == today_date:
                            self.today_rate = float(currency_data[4].replace(",", "."))
                            self.today_rate_valid = True
                            log.info(f'EnergyRouting: received daily EUR/CZK exchange rate from CNB: {self.today_rate} CZK/EUR')
                            self.openhab_current_czk_to_eur_rate_today_item.oh_send_command(self.today_rate)
                        else:
                            self.previous_rate = float(currency_data[4].replace(",", "."))
                            self.previous_rate_valid = True
                            self.today_rate_valid = False
                            log.info(f'EnergyRouting: received last valid EUR/CZK exchange rate from CNB: {self.previous_rate} CZK/EUR')
                            self.openhab_current_czk_to_eur_rate_today_previous_item.oh_send_command(self.previous_rate)
                        break
                
               
        except OSError as err:
            log.error(f'EnergyRouting: error receiving EUR/CZK rate from CNB: "{err}"')
            self.today_rate_valid = False
            self.previous_rate_valid = False
        # download today and yesterday rates
        # https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date=12.11.2020
