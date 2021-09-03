'''
DHT11 hygrometer & thermometer module.

PINOUT:
    DHT | RPI
1   VCC | 2 (5.0V)
2   SIG | 7 (GPIO)
3   -   | - 
4   GND | 9 (GND)

Inserted 10K Ohm pull-up resistor binding together VCC and SIG.
'''
import time
import board
import adafruit_dht
from transmitter.sensors.sensor import Sensor

class Hygrometer(Sensor):
    def __init__(self):
        Sensor.__init__(self)
        self.name = 'HYG'
        self.running = True
        self.topic = f'/{self.name}'
        self.sensor_id = self.name
        self.location = 'Wrocław'

        # Init Device
        self.dev = adafruit_dht.DHT11(board.D4)

    def get_sensor_data(self):
        try:
            time.sleep(1.0)
            temperature = self.dev.temperature
            humidity = self.dev.humidity
            if temperature is not None and humidity is not None:
                return [
                    ('temperature', temperature),
                    ('humidity', humidity)
                ]
        except RuntimeError as error:
            print(error.args[0])
        except Exception as error:
            self.dev.exit()
            raise error
