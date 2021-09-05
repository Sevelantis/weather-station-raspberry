import logging
import sys
from observers.observable import Observer
from DTO.message import Message

logging.basicConfig(level=logging.INFO, filename='/home/pi/weather-station/logs/WS.log', filemode='w', format='%(asctime)s - %(levelname)s --- Logger - Msg: %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

class Logger(Observer):
    def __init__(self) -> None:
        pass

    def notify(self, msg) -> None:
        if isinstance(msg, Message):
            logging.info(f'{msg.logging_stage},{msg.location},{msg.topic},{msg.sensor_id},{msg.location},{msg.type},{msg.value}')
        if isinstance(msg, str):
            logging.info(msg)
