import logging
import sys
from observers.observable import Observer, ObserversList
from DTO.message import Message

logging.basicConfig(level=logging.INFO, filename='./logs/WS.log', filemode='w', format='%(asctime)s - %(levelname)s --- Logger - Msg: %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

class Logger(Observer):
    def __init__(self) -> None:
        Observer.__init__(self, ObserversList.LOGGER)

    def notify(self, msg: Message) -> None:
        logging.info(f'{msg.logging_stage},{msg.location},{msg.topic},{msg.sensor_id},{msg.location},{msg.type},{msg.value}')
