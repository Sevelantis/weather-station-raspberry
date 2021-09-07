import influxdb
import paho.mqtt.client as mqtt
from threading import *
from sig.signal_handler import handler
import time
import random
import string
import logging
from influxdb import InfluxDBClient
from DTO.message import Message, LoggingStage
from observers.observable import Observable

INFLUXDB_ADDRESS = 'localhost'
INFLUXDB_PORT = 8086
INFLUXDB_USER = 'admin'
INFLUXDB_PASSWORD = 'admin123'
INFLUXDB_DATABASE = 'sensors'

MQTT_ADDRESS = 'localhost'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'WS_mqtt_over_containers-catcher'

class Catcher(Thread, Observable):
    def __init__(self, observers):
        Thread.__init__(self)
        Observable.__init__(self, observers)
        self.name = 'HYG'
        self.running = True

        self.connected = False
        self.received = False
        self._init_influxdb_agent()
        self._init_mqtt()

    def on_message(self, client, userdata, json) -> None:
        msg = Message()
        msg.deserialize(json.payload.decode('utf-8'))
        msg.logging_stage=LoggingStage.RECEIVED.value
        self._send_data_to_influxdb(msg)
        self.notify_observers(msg)

    def _send_data_to_influxdb(self, message: Message) -> None:
        array = self._parse_msg(message)
        self.influxdb_agent.write_points(array, database=INFLUXDB_DATABASE, time_precision='ms', batch_size=10000, protocol='line')

    def _parse_msg(self, msg: Message):
        return [
            "{measurement},location={location},sensor_id={sensor_id},type={type} value={value}i {timestamp}"
            .format(measurement=msg.topic,
                    location=msg.location,
                    sensor_id=msg.sensor_id,
                    type=msg.type,
                    value=int(msg.value),
                    timestamp=int(time.time_ns()/1000000))]

    def run(self):
        while self.running:
            if handler.SIGINT:
                self.running = False
                break
            time.sleep(0.5)

        # on quit
        self.mqtt.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        self.notify_observers(f'Catcher: Connected with RC = {rc}')
        
        if rc == 0:
            self.connected = True
            client.subscribe('/+')
            self.notify_observers(f'Catcher: was already connected to MQTT. RC = {rc}')
        else:
            self.notify_observers(f'Catcher: MQTT connection failed. RC = {rc}')

    def _init_influxdb_agent(self):
        self.influxdb_agent = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
        
        # sensors_database = [db for db in self.influxdb_agent.get_list_database() if db['name'] == INFLUXDB_DATABASE]
        # if INFLUXDB_DATABASE not in sensors_database:
        #     logging.info(f'Database {INFLUXDB_DATABASE} not exists. Creating db: {INFLUXDB_DATABASE}' )
        #     self.influxdb_agent.create_database(INFLUXDB_DATABASE)
        # else: 
        #     logging.info(f'Database {INFLUXDB_DATABASE} has already been created.')
        # self.influxdb_agent.create_database(INFLUXDB_DATABASE)
   
        self.influxdb_agent.switch_database(INFLUXDB_DATABASE)
    
    def _init_mqtt(self):
        self.mqtt = mqtt.Client(MQTT_CLIENT_ID)
        self.mqtt.loop_stop()
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_message = self.on_message
        self.mqtt.connect(MQTT_ADDRESS, MQTT_PORT)
        self.mqtt.loop_start()
        while self.connected != True:
            time.sleep(.2)
