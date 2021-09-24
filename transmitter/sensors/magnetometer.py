'''
Magnetometer HMC5883L module. I2C protocol

PINOUT:
    MAG |   RPI
1   VCC |   2 (5.0V)
2   GND |   14 (GND)
3   SCL |   27 (I2C dev 0)
4   SDA |   28 (I2C dev 0)
5   DRDY|   -

'''
from transmitter.sensors.modules.HMC5883L import HMC5883L
from transmitter.sensors.sensor import Sensor


class Magnetometer(Sensor):
    def __init__(self, HMC_observers):
        Sensor.__init__(self)
        self.name = 'MAG'
        self.running = True
        self.topic = f'/{self.name}'
        self.sensor_id = self.name
        self.location = 'Wrocław'
        self.HMC_observers = HMC_observers

    def run(self):
        # Init Device
        self.dev = HMC5883L(port=0, observers=self.HMC_observers)
        super().run()
        # close i2c
        self.dev.close()

    def get_sensor_data(self):
        try:
            (x, y, z) = self.dev.get_axes()
            # heading = self.dev.getHeading()
            if x and y and z:
                return [
                        ('x', x),
                        ('y', y),
                        ('z', z)
                    ]
        except RuntimeError as error:
            print(error.args[0])
        except Exception as error:
            print(f"Exception: {error}")
            raise error
