'''
Comment
'''
import time
import board
import adafruit_dht
from transmitter.sensors.sensor import Sensor


class Barometer(Sensor):
    def __init__(self):
        Sensor.__init__(self)
        self.name = 'BAR'
        self.running = True
        # Init Device
        self.topic = f'/{self.name}'
        self.sensor_id = self.name
        self.location = 'Wrocław'

        self.dev = adafruit_dht.DHT11(board.D4)

    def get_data(self):
        pass