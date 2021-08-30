import re
import time
from typing import NamedTuple
import paho.mqtt.client as mqtt
import logging
from observers.observable import Observer, Observable
from DTO.message import LoggingStage, Message

MQTT_ADDRESS = 'localhost'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'publish_sensor_data_to_broker'

class Publisher(Observable, Observer):
    def __init__(self):
        Observable.__init__(self)
        self.connected = False
        self._init_mqtt()

    def notify(self, msg: Message) -> None:
        msg.logging_stage = LoggingStage.SENT.value

        self.mqtt.publish(msg.topic, msg.serialize())

        self.notify_observers(msg)

    def on_publish(self, client, data, result):
        pass

    def on_connect(self, client, userdata, flags, rc):
        self.notify_observers(f'Connected with RC = {rc}')

        if rc == 0:
            self.connected = True
            self.notify_observers(f'Was already connected to MQTT. RC = {rc}')
        else:
            self.notify_observers(f'MQTT connection failed. RC = {rc}')

    def _init_mqtt(self):
        self.mqtt = mqtt.Client(MQTT_CLIENT_ID)
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_publish = self.on_publish
        self.mqtt.connect(MQTT_ADDRESS, MQTT_PORT)
        self.mqtt.loop_start()
        while self.connected != True:
            time.sleep(.2)
        self.mqtt.loop_stop()
    