from enum import Enum
from DTO.dto import DTO

class LoggingStage(Enum):
    COLLECTED = 'COLLECTED'
    SENT = 'SENT'
    RECEIVED = 'RECEIVED'

class Message(DTO):
    def __init__(self, topic=None, sensor_id=None, location=None, type=None, value=None, logging_stage=None) -> None:
        self.topic = topic
        self.sensor_id = sensor_id
        self.location = location
        self.type = type
        self.value =  value
        self.logging_stage = logging_stage
