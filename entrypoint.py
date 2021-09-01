'''
This module reads data from RPi sensors - real-time\
'''
from transmitter.publisher import Publisher
from receiver.catcher import Catcher
from transmitter.sensors.hygrometer import Hygrometer
from transmitter.sensors.barometer import Barometer
from observers.logger import Logger

if __name__ == '__main__':
    logger = Logger()
    publisher = Publisher([logger])
    catcher = Catcher([logger])
    catcher.start()

    # running = True
    # while running:
    #     if handler.SIGINT:
    #         running = False
    #         break
    #     time.sleep(0.5)
    #     publisher.publish('/home/pi/weather-station/data/test', random.randint(0,1000))

    sensors = [Hygrometer()]

    catcher.add_observer(logger)
    publisher.add_observer(logger)

    # run devices threads
    for sensor in sensors:
        sensor.add_observer(publisher)
        sensor.start()
    
    # join devices threads
    for sensor in sensors:
        sensor.join()

    catcher.join()
    print('EXIT SUCCEESS')