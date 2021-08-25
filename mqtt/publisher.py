import re
import time
from typing import NamedTuple
import paho.mqtt.client as mqtt
import logging

MQTT_ADDRESS = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC = 'home/+/+'
MQTT_REGEX = 'home/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'publish_sensor_data_to_broker'

logging.basicConfig(level=logging.INFO, format='Publisher: %(message)s ')

class Publisher:
    def __init__(self):
        logging.info('init')
        self.connected = False
        self._init_mqtt()

    def _init_mqtt(self):
        self.mqtt = mqtt.Client(MQTT_CLIENT_ID)
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_publish = self.on_publish
        self.mqtt.connect(MQTT_ADDRESS, MQTT_PORT)
        self.mqtt.loop_start()
        while self.connected != True:
            time.sleep(.2)
        self.mqtt.loop_stop()
    
    def on_connect(self, client, userdata, flags, rc):
        print(f'Connected with RC = {rc}')
        if rc == 0:
            logging.info('Was already connected to MQTT.')
            self.connected = True
        else:
            logging.info(f'MQTT connection failed. RC = {rc}')

    def publish(self, msg):
        self.mqtt.publish('/home/pi/weather-station/data', msg)
        
    def on_publish(self, client, data, result):
        logging.info(f'data published, msg = {result}')
