'''
Barometer BMP280 module. I2C protocol

PINOUT:
    BMP | RPI
1   VCC | 1 (3.3V)
2   GND | 9 (GND)
3   SCL | 5 (SCL)
4   SCK | 3 (SDA)
'''
import logging
import board
import adafruit_bmp280
from transmitter.sensors.sensor import Sensor

class Barometer(Sensor):
    def __init__(self):
        Sensor.__init__(self)
        self.name = 'BAR'
        self.running = True
        self.topic = f'/{self.name}'
        self.sensor_id = self.name
        self.location = 'Wrocław'

        # Init Device
        i2c = board.I2C()       
        self.dev = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address = 0x76)

    def get_sensor_data(self):
        try:
            pressure = float(self.dev.pressure)
            temperature = float(self.dev.temperature)
            if pressure:
                return [
                        ('temperature', temperature),
                        ('pressure', pressure)
                    ]
        except RuntimeError as error:
            logging.info(f"{self.name}: {error.args[0]}")
        except Exception as error:
            logging.info(f"{self.name}: {error}")
            self.dev.exit()
            raise error
