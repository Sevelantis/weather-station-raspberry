from signals.signal_handler import signal_handler
import paho.mqtt.client as mqtt
from threading import *
import time
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
        points = self._parse_msg(message)
        self.influxdb_agent.write_points(points, database=INFLUXDB_DATABASE, protocol='line',time_precision='ms', batch_size=10000)

    def _parse_msg(self, msg: Message):
        return [f"{msg.topic},location={msg.location},sensor_id={msg.sensor_id},type={msg.type} value={msg.value} {int(time.time() * 1000)}"]

    def run(self):
        while self.running:
            if signal_handler.SIGINT:
                self.running = False
                self.notify_observers("Catcher: SIGINT detected. Exiting catcher's thread.")
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
        self.influxdb_agent = InfluxDBClient(host=INFLUXDB_ADDRESS, port=INFLUXDB_PORT, username=INFLUXDB_USER, password=INFLUXDB_PASSWORD)
        
        # check if sensors db exists
        dbs = self.influxdb_agent.get_list_database()
        sensors_db_exists = False
        for db in dbs:
            if db['name'] == INFLUXDB_DATABASE:
                sensors_db_exists = True
                break
        if not sensors_db_exists:
            self.notify_observers(f'Catcher: Creating database {INFLUXDB_DATABASE}. It didn\'t exist.')
            self.influxdb_agent.create_database(INFLUXDB_DATABASE)
        else:
            self.notify_observers(f'Catcher: Database {INFLUXDB_DATABASE} already exists.')
        # switch db
        self.influxdb_agent.switch_database(INFLUXDB_DATABASE)
        self.notify_observers(f'Catcher: Switching to DB {INFLUXDB_DATABASE}')
    
    def _init_mqtt(self):
        self.mqtt = mqtt.Client(MQTT_CLIENT_ID)
        self.mqtt.loop_stop()
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_message = self.on_message
        self.mqtt.connect(MQTT_ADDRESS, MQTT_PORT)
        self.mqtt.loop_start()
        while self.connected != True:
            time.sleep(.2)
