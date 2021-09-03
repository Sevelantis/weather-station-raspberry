'''
Barometer BMP280 module.

PINOUT:
    BMP | RPI
1   VCC | 1 (3.3V)
'''
import time
import board
from transmitter.sensors.sensor import Sensor

class Ultrasonic(Sensor):
    def __init__(self):
        Sensor.__init__(self)
        self.name = 'ULT'
        self.running = True
        # Init Device
        self.topic = f'/{self.name}'
        self.sensor_id = self.name
        self.location = 'Wrocław'



    def get_sensor_data(self):
        time.sleep(1.0)
        try:
            # TODO::
            pass
        except RuntimeError as error:
            print(error.args[0])
        except Exception as error:
            self.dev.exit()
            raise error