import re
import time
from typing import NamedTuple
import paho.mqtt.client as mqtt
import logging

MQTT_ADDRESS = 'localhost'
MQTT_PORT = 1883
MQTT_USER = 'root'
MQTT_PASSWORD = 'mqtt123!'
MQTT_TOPIC = 'home/+/+'
MQTT_REGEX = 'home/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'publish_sensor_data_to_broker'

logging.basicConfig(level=logging.INFO, format='Publisher: %(message)s ')

class Publisher:
    def __init__(self):
        logging.info('Publisher init')    
        self._init_mqtt()

        while self.connected != True:
            time.sleep(.2)
        self.mqtt.loop_stop()

    def _init_mqtt(self):
        self.mqtt = mqtt.Client(MQTT_CLIENT_ID)
        self.mqtt.loop_stop()
        self.mqtt.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_publish = self.on_publish
        self.mqtt.connect(MQTT_ADDRESS, MQTT_PORT)
        self.connected = False
        self.mqtt.loop_start()
    
    def on_connect(self, client, userdata, flags, rc):
        """ The callback for when the client receives a CONNACK response from the server."""
        if rc == 0:
            logging.info('Was already connected to MQTT.')
            self.connected = True
        else:
            logging.info('MQTT connection failed.')

    def publish(self, msg):
        self.mqtt.publish('/home/pi/weather-station/data', msg)
        logging.info('sent...')
        

    def on_publish(self, client, data, result): # callback
        logging.info('data published')

    # def _parse_mqtt_message(self, topic, payload):
    #     """TODO"""
    #     match = re.match(MQTT_REGEX, topic)
    #     if match:
    #         location = match.group(1)
    #         measurement = match.group(2)
    #         if measurement == 'status':
    #             return None
    #         return SensorData(location, measurement, float(payload))
    #     else:
    #         return None
   
    # --todo turn into sed
    # '  # urls = ["http://127.0.0.1:8086"]' -> '  urls = ["http://influxdb:8086"]'
    # '  # database = "telegraf"' -> '  database = "sensors"'
    # '  # skip_database_creation = false' -> '  skip_database_creation = true'
    # '  # username = "telegraf"' -> '  username = "telegraf"'
    # '  # password = "metricsmetricsmetricsmetrics"' -> '  password = "telegraf123"'
    # '#   servers = ["tcp://127.0.0.1:1883"]' -> '  servers = ["tcp://mqtt:1883"]'
    # '#   data_format = "influx"' -> '  data_format = "influx"'

