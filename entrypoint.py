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
    logging.info('elo..')
    publisher = Publisher()

    while 1:
        time.sleep(1)
        publisher.publish(f'my random number is :) {str(random.randint(-20,20))}')

    # sensors = [Hygrometer(), Thermometer(), Barometer(), Gas_sensor()]
    
    # # run devices threads
    # for sensor in sensors:
    #     sensor.start()
    
    # # join devices threads
    # for sensor in sensors:
    #     sensor.join()

    # logging.info('EXIT SUCCESS')
