'''
Barometer BMP280 module. I2C protocol

PINOUT:
    BMP | RPI
1   VCC | 1 (3.3V)
2   GND | 9 (GND)
3   SCL | 5 (SCL)
4   SCK | 3 (SDA)
'''
import time
import board
import adafruit_bmp280
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

        i2c = board.I2C()       
        self.dev = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address = 0x76)

    def get_sensor_data(self):
        time.sleep(1.0)
        try:
            pressure = self.dev.pressure
            temperature = self.dev.temperature
            if pressure is not None:
                return [
                        ('temperature', temperature),
                        ('pressure', pressure)
                    ]
        except RuntimeError as error:
            print(error.args[0])
        except Exception as error:
            self.dev.exit()
            raise error
