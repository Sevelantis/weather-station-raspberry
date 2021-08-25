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
        self._init_influxdb_agent()
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
            client.subscribe('/home/pi/weather-station/data/test')
            logging.info(f'Catcher was already connected to MQTT. RC = {rc}')
        else:
            logging.info(f'Catcher MQTT connection failed. RC = {rc}')

    def on_message(self, client, userdata, msg):
        logging.info('msg received - > ' + msg.topic + ' ' + str(msg.payload.decode('utf-8')))
        data = self._parse_msg(msg.topic, msg.payload.decode('utf-8'))
        # TODO KNOW INFLUXDB DATA FORMAT TO SEND
        if data is not None:
            self._send_data_to_influxdb(data)

    def _send_data_to_influxdb(self, data):
        self.influxdb_agent.write_points(data, database=INFLUXDB_DATABASE, time_precision='ms', batch_size=10000, protocol='line')

    def _parse_msg(self, topic, msg):
        import random
        data = []
        data.append("{measurement},location={location},fruit={fruit},id={id} x={x},y={y},a={a},b={b},c={c},d={d},e={e}i {timestamp}"
            .format(measurement=topic,
                    location='Wrocław',
                    fruit='testfruit',
                    id='testtag',
                    x=random.randint(0,100),
                    y=random.randint(100,150),
                    a=random.randint(250,444),
                    b=random.randint(300,600),
                    c=random.randint(500,700),
                    d=random.randint(700,800),
                    e=random.randint(799,899),
                    timestamp=int(time.time_ns()/1000000)))
        return data

    def _init_influxdb_agent(self):
        logging.info('INIT AGENT')
        self.influxdb_agent = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
        
        sensors_database = [db for db in self.influxdb_agent.get_list_database() if db['name'] == INFLUXDB_DATABASE]
        if INFLUXDB_DATABASE not in sensors_database:
            logging.info(f'Database {INFLUXDB_DATABASE} not exists. Creating db: {INFLUXDB_DATABASE}' )
            self.influxdb_agent.create_database(INFLUXDB_DATABASE)
        else: 
            logging.info(f'Database {INFLUXDB_DATABASE} has already been created.')
        
        self.influxdb_agent.switch_database(INFLUXDB_DATABASE)
    
    def run(self):
        while self.running:
            if handler.SIGINT:
                self.running = False
                break
            time.sleep(0.5)

        # on quit
        self.mqtt.loop_stop()
