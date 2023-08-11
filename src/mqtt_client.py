from logger import log
import paho.mqtt.client as mqtt
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

broker_url = config['MQTT']['broker_url']
broker_port = int(config['MQTT']['broker_port'])
topic = config['MQTT']['topic']

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(broker_url, broker_port)

    def publish_price(self, price):
        self.client.publish(topic, str(price))

    def get_current_price(self):
        # Implement get current price function using MQTT's retained messages
        pass

    def get_prices_for_day(self):
        # Implement get prices for the whole day function using MQTT's retained messages
        pass

    def get_prices_for_next_day(self):
        # Implement get prices for the next day function using MQTT's retained messages
        pass
