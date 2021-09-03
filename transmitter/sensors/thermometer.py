'''
DS18B20thermometer module.

PINOUT: (FLAT SIDE IS FRONT, COUNT FROM LEFT)
    DS18| RPI
1   GND | 1 (GND)
2   SIG | 12 (BCM 1)
3   VCC | 9 (3.3V)

Inserted 10K Ohm pull-up resistor binding together VCC and SIG.
'''
import time
import RPi.GPIO as GPIO
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

        # Init Device
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        self.SIG_PIN = 1
        GPIO.setup(self.SIG_PIN, GPIO.OUT)
        GPIO.output(self.SIG_PIN, GPIO.HIGH)
        
        self.dev = W1ThermSensor()

    def get_sensor_data(self):
        try:
            time.sleep(1.0)
            temperature = self.dev.get_temperature()
            if temperature is not None:
                return [
                    ('temperature', temperature)
                ]
        except RuntimeError as error:
            print(error.args[0])
        except Exception as error:
            self.dev.exit()
            raise error
