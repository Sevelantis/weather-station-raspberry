import logging
from observers.observable import Observer

sensor_ids = {
    'HYG': 'HYG',
    'BAR': 'BAR',
    'THE': 'THE',
    'GAS': 'GAS',
    'ULT': 'ULT',
}

password = 'Logo123Logo321'
passwordd= 'avtoxtsvvaemhtfc'

BAR_ALERT = 1020.0

class Mailer(Observer):
    def __init__(self) -> None:
        pass

    def filter_sensor_messages(self, id, topic, value)->None:
        if not value:
            return
        if id == sensor_ids['BAR']:
            # if topic == ''
            pass
        elif id == sensor_ids['HYG']:
            pass
        elif id == sensor_ids['THE']:
            pass
        elif id == sensor_ids['GAS']:
            pass
        elif id == sensor_ids['ULT']:
            pass

    def notify(self, msg) -> None:
        logging.info(f'{msg.logging_stage}->{msg.location},{msg.topic},{msg.sensor_id},{msg.location},{msg.type},{msg.value}')
        self.filter_sensor_messages(id=msg.sensor_id, topic=msg.topic, value=msg.value)
    

