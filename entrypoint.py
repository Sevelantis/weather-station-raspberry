'''
This module reads data from RPi sensors - real-time\
'''
import logging
from sensors.hygrometer import *
from sensors.thermometer import *
from sensors.barometer import *
from sensors.gas_sensor import *
from mqtt.publisher import *
from mqtt.broker import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(name)s:%(message)s ')

if __name__ == '__main__':
    # broker = Broker()
    publisher = Publisher()

    publisher.publish('HELLO WORLD  c:     //')

    # sensors = [Hygrometer(), Thermometer(), Barometer(), Gas_sensor()]
    
    # # run devices threads
    # for sensor in sensors:
    #     sensor.start()
    
    # # join devices threads
    # for sensor in sensors:
    #     sensor.join()

    # logging.info('EXIT SUCCESS')
