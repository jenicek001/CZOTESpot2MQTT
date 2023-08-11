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
            exchange_rate_czk_eur = exchange_rate.fetch_exchange_rate()

            electricity_price_czk = await electricity_prices.async_update_spot_electricity_costs()

            # Publish the price in CZK via MQTT
            mqtt_client.publish_price(electricity_price_czk)

            time.sleep(3600)  # Sniff hourly prices (wait for 1 hour)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    log.info("Starting the application...")

    asyncio.run(main())
