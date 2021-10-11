'''
Ultrasonic sensor HC-SR04

PINOUT:
    HC  | RPI
1   VCC | 2 (5.0V)
2   ECHO| 18 (GPIO) (24 BCM)
3   TRIG| 8 (GPIO) (14 BCM)
4   GND | 14 (GND)

Inserted two pull-up resistors 470ohm and 470ohm, binding together ECHO and GND
This is because HR-SR04 works at 5V and GPIO pins works at max 3.3V
ECHO->470->GPIO->470->GND
'''
import board
from adafruit_hcsr04 import HCSR04
from transmitter.sensors.sensor import Sensor
import logging

class Ultrasonic(Sensor):
    def __init__(self):
        Sensor.__init__(self)
        self.name = 'ULT'
        self.running = True
        self.topic = f'/{self.name}'
        self.sensor_id = self.name
        self.location = 'Wrocław'

    def get_sensor_data(self):
        try:
            distance = self.dev.distance
            if distance:
                return [
                    ('distance', distance)
                ]
            else:
                logging.info(f"{self.name}: No data returned.")
        except RuntimeError as error:
            logging.info(f"{self.name}: {error.args[0]}")
        except Exception as error:
            logging.info(f"{self.name}: {error}")

    def run(self) -> None:
        # Init Device
        try:
            self.dev = HCSR04(trigger_pin=board.D14, echo_pin=board.D24)
        except Exception as e:
            logging.info(f'{self.name}: Init failed, reason: {e}')
        super().run()