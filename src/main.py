from logger import log
from electricity_prices import ElectricityPrices
from exchange_rate import ExchangeRate
from mqtt_client import MQTTClient
import asyncio
import time

async def main():
    
    electricity_prices = ElectricityPrices()
    exchange_rate = ExchangeRate()
    mqtt_client = MQTTClient()

    while True:
        try:
            # Fetch electricity prices and exchange rate
            #electricity_price_czk = electricity_prices.fetch_prices()
            exchange_rate_czk_eur = await exchange_rate.async_update_exchange_rate()
            log.info(f"Exchange rate: {exchange_rate_czk_eur} CZK/EUR")

            if exchange_rate_czk_eur is not None:

                result = await electricity_prices.async_update_spot_electricity_costs()
                if result:
                    electricity_price_eur = electricity_prices.get_current_price() # in EUR
                    electricity_price_czk = electricity_price_eur * exchange_rate_czk_eur / 1000.0
                    log.info(f"Electricity price 1kWh: {electricity_price_czk} CZK")

                    # Publish the price in CZK via MQTT
                    mqtt_client.publish_price(electricity_price_czk)
                else:
                    log.error("Failed to fetch electricity prices from OTE-ČR")
            else:
                log.error("Failed to fetch exchange rate from ČNB")

            time.sleep(3600)  # Sniff hourly prices (wait for 1 hour)

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    log.info("Starting the application...")

    asyncio.run(main())
