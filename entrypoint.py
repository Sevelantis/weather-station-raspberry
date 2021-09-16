'''
This module reads data from RPi sensors - real-time
'''
from transmitter.publisher import Publisher
from transmitter.sensors.hygrometer import Hygrometer
from transmitter.sensors.barometer import Barometer
from transmitter.sensors.ultrasonic import Ultrasonic
from transmitter.sensors.thermometer import Thermometer
from transmitter.sensors.gas_sensor import Gas_sensor
from observers.logger import Logger
from receiver.catcher import Catcher

if __name__ == '__main__':
    logger = Logger()
    publisher = Publisher([logger])
    catcher = Catcher([logger])
    catcher.start()

    sensors = [Hygrometer(), Barometer(), Ultrasonic(), Thermometer(), Gas_sensor([logger])]
    # sensors = [Hygrometer()]

    # run devices threads
    for sensor in sensors:
        sensor.add_observer(publisher)
        sensor.start()
    
    catcher.join()
    
    # join devices threads
    for sensor in sensors:
        sensor.join()

    logger.notify("Logger: Ended session. Goobye!!")
