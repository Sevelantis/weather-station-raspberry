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
import time
import RPi.GPIO as GPIO
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

        # Init Device
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        #set GPIO Pins
        self.GPIO_ECHO = 24
        self.GPIO_TRIGGER = 14

        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

    def get_sensor_data(self):
        try:
            distance = self.get_distance()
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
            self.dev.exit()
            raise error

    def get_distance(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance