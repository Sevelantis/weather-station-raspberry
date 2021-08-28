'''
This module reads data from RPi sensors - real-time\
'''
import logging
from sensors.hygrometer import *
from sensors.thermometer import *
from sensors.barometer import *
from sensors.gas_sensor import *
from mqtt.publisher import *
from mqtt.catcher import *
import random
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(name)s:%(message)s ')

if __name__ == '__main__':
    publisher = Publisher()

    catcher = Catcher()
    catcher.start()

    # running = True
    # while running:
    #     if handler.SIGINT:
    #         running = False
    #         break
    #     time.sleep(0.5)
    #     publisher.publish('/home/pi/weather-station/data/test', random.randint(0,1000))

    # sensors = [Hygrometer(publisher), Thermometer(publisher), Barometer(publisher), Gas_sensor(publisher)]
    sensors = [Hygrometer(publisher)]
    # run devices threads
    for sensor in sensors:
        sensor.start()
    
    # join devices threads
    for sensor in sensors:
        sensor.join()

    catcher.join()
    logging.info('EXIT SUCCESS')
