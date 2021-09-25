'''
DS18B20thermometer module.

PINOUT: (FLAT SIDE IS FRONT, COUNT FROM LEFT)
    DS18| RPI
1   GND | 1 (GND)
2   SIG | 12 (BCM 1)
3   VCC | 9 (3.3V)

Inserted 10K Ohm pull-up resistor binding together VCC and SIG.
'''
import logging
from w1thermsensor import W1ThermSensor
from transmitter.sensors.sensor import Sensor

class Thermometer(Sensor):
    def __init__(self):
        Sensor.__init__(self)
        self.name = 'THE'
        self.running = True
        self.topic = f'/{self.name}'
        self.sensor_id = self.name
        self.location = 'Wrocław'
            
    def run(self) -> None:
        try:
            self.dev = W1ThermSensor()
        except Exception as e:
            logging.info(f'{self.name}: Thermometer init failed.')
        super().run()

    def get_sensor_data(self):
        try:
            temperature = self.dev.get_temperature()
            if temperature:
                return [
                    ('temperature', temperature)
                ]
            else:
                logging.info(f"{self.name}: No data returned.")
        except RuntimeError as error:
            logging.info(f"{self.name}: {error.args[0]}")
        except Exception as error:
            logging.info(f"{self.name}: {error}")
            self.dev.exit()
            raise error
