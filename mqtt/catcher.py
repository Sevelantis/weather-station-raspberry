import paho.mqtt.client as mqtt
from threading import *
from signal_handler import handler
import time
import logging
from influxdb import InfluxDBClient

logging.basicConfig(level=logging.INFO, format='Catcher: %(message)s ')

INFLUXDB_ADDRESS = 'localhost'
INFLUXDB_PORT = 8086
INFLUXDB_USER = 'admin'
INFLUXDB_PASSWORD = 'admin123'
INFLUXDB_DATABASE = 'sensors'

MQTT_ADDRESS = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC = 'home/+/+'
MQTT_REGEX = 'home/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'mqtt_to_influxdb_publisher'

class Catcher(Thread):
    def __init__(self):
        super().__init__()
        self.name = 'HYG'
        self.running = True
        logging.info('init')
        # self._init_influxdb_database()
        self.connected = False
        self.received = False
        self._init_mqtt()

    def _init_mqtt(self):
        self.mqtt = mqtt.Client(MQTT_CLIENT_ID)
        self.mqtt.loop_stop()
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_message = self.on_message
        self.mqtt.connect(MQTT_ADDRESS, MQTT_PORT)
        self.mqtt.loop_start()
        while self.connected != True:
            time.sleep(.2)

    def on_connect(self, client, userdata, flags, rc):
        print(f'Connected with RC = {rc}')
        if rc == 0:
            self.connected = True
            client.subscribe('/home/pi/weather-station/data')
            logging.info(f'Catcher was already connected to MQTT. RC = {rc}')
        else:
            logging.info(f'Catcher MQTT connection failed. RC = {rc}')

    def on_message(self, client, userdata, msg):
        logging.info('msg received - > ' + msg.topic + ' ' + str(msg.payload.decode('utf-8')))
        # sensor_data = self._parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
        # if sensor_data is not None:
        #     self._send_sensor_data_to_influxdb(sensor_data)

    # def _init_influxdb_database(self):
    #     self.influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
    #     self.influxdb_client.switch_database(INFLUXDB_DATABASE)
    
    def run(self):
        while self.running:
            if handler.SIGINT:
                self.running = False
                break
            time.sleep(0.02)

        # on quit
        self.mqtt.loop_stop()


# if __name__ == '__main__':
#     Catcher = Catcher()
