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
from threading import *
from handler.signal_handler import handler
import time
import board
import adafruit_dht

class Hygrometer(Thread):
    def __init__(self):
        super().__init__()
        self.name = 'HYG'
        self.running = True
        # Init Device
        self.dev = adafruit_dht.DHT11(board.D4)

    def run(self):
        while self.running:
            self.read_data()
            if handler.SIGINT:
                self.running = False
                break
                
    def read_data(self):
        try:
            temperature_c = self.dev.temperature
            humidity = self.dev.humidity
            print("Sensor: {} Temp: {:.1f} C    Humidity: {}% ".format(
                    super().name, temperature_c, humidity))

        except RuntimeError as error:
            print(error.args[0])
        except Exception as error:
            self.dev.exit()
            raise error

        time.sleep(1.0)

