'''
Creates and starts:
    - Threads for sensor instances - sensors notifes theirs observers.
    - Publisher that publishses data via the MQTT broker. Indexes the message with topic.
    - Catcher that catches published data via topic subscribtion, then sends the data to Influxdb server.

In order to clean exit SIGINT signal is being watched.
Whenever SIGINT is detected during the run, the app starts to perform clean exit - every thread does its clean quit.
'''
from transmitter.publisher import Publisher
from transmitter.sensors.hygrometer import Hygrometer
from transmitter.sensors.barometer import Barometer
from transmitter.sensors.ultrasonic import Ultrasonic
from transmitter.sensors.thermometer import Thermometer
from transmitter.sensors.gas_sensor import Gas_sensor
from transmitter.sensors.magnetometer import Magnetometer
from observers.logger import Logger
from receiver.catcher import Catcher

if __name__ == '__main__':
    logger = Logger()
    publisher = Publisher([logger])
    catcher = Catcher([logger])
    catcher.start()

    sensors = [Magnetometer(HMC_observers=[logger]), Gas_sensor(MQ_observers=[logger]), Ultrasonic(), Hygrometer(), Barometer(), Thermometer()]

    # run devices threads
    for sensor in sensors:
        sensor.add_observer(publisher)
        sensor.start()
    
    catcher.join()
    
    # join devices threads
    for sensor in sensors:
        sensor.join()

    logger.notify("Logger: Ended session. Goobye!!")
