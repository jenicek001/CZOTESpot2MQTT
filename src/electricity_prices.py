import aiohttp
import asyncio
import configparser
from logger import log
from datetime import date, datetime, timedelta
import json

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
 
    async def async_update_spot_electricity_costs(self):
        log.info("Fetching spot electricity costs from OTE-CR...")

        today_date_local = date.today()
        timestamp_now = datetime.now()

        success = False

        try:
            async with aiohttp.ClientSession() as session:
                request_time = datetime.now()
                async with session.get(f'https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data?report_date={today_date_local}') as resp:
                    log.debug(f'get: {resp.status}')
                    #print(resp.status)
                    #print(await resp.text())

                    log.debug(f'OTE price cost response: "{resp}"')
                    result = await resp.json()
                    request_duration = datetime.now() - request_time
                    log.debug(f'OTE price cost request duration: "{request_duration}"')
                    log.debug(f'OTE price cost result: "{result}"')

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
                                            log.debug(f'OTE price cost received daily spot electricity prices from OTE-CR: hour: {i:02d}:00-{(i+1):02d}:00 {self.spot_electricity_price_today[i]} EUR/MWh')
                                            success = True
                                        # self.report_hourly_spot_electricity_costs()
                                    else:
                                        log.error(f'OTE price cost expected 24 values for daily spot prices, received {len(hourly_spot_price)}')
                                else:
                                    log.error(f'OTE price cost missing "point" array in JSON from OTE-CR')
                            else:
                                log.error(f'OTE price cost "dataLine" in JSON from OTE-CR does not have expected 2 items - amount and price')
                        else:
                            log.error(f'OTE price cost missing "dataLine" array in JSON from OTE-CR')
                    else:
                        log.error(f'OTE price cost missing "data" in JSON from OTE-CR')

        except OSError as err:
            log.error(f'OTE price cost error receiving data from OTE-CR: "{err}"')

            if timestamp_now - self.spot_electricity_price_last_update_time > timedelta(hours=24):
                return False

        except Exception as err:
            log.error(f'OTE price cost error receiving data from OTE-CR: "{err}"')

            if timestamp_now - self.spot_electricity_price_last_update_time > timedelta(hours=24):
                return False
            
        return success

    def get_current_price(self):
        return self.spot_electricity_price_today[datetime.now().hour]