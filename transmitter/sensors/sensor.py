from DTO.message import Message, LoggingStage
from sig.signal_handler import handler
from observers.observable import Observable, ObserversList
from threading import *

class Sensor(Thread, Observable):
    def __init__(self):
        Thread.__init__(self)
        Observable.__init__(self)

    def run(self) -> None:
        while self.running:
            self.read_data()
            if handler.SIGINT:
                self.running = False
                break

    def build_message(self, type, value, logging_stage=None) -> Message:
        return Message(topic=self.topic, sensor_id=self.sensor_id, location=self.location, type=type, value=value, logging_stage=logging_stage)

    def read_data(self) -> None:
        sensor_data = self.get_sensor_data()
        if sensor_data:
            for type, value in sensor_data:
                self.notify_observer(self.build_message(type=type, value=value, logging_stage=LoggingStage.COLLECTED.value), ObserversList.PUBLISHER)
