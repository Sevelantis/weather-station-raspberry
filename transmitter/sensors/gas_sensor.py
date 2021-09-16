'''
MQ-2 gas sensor module. LPG, CO, SMOKE measurements.

PINOUT:
    MQ-2    | RPI           |   MCP3008
1   VCC     | 2 (5.0V)      |   -
2   GND     | 20(GND)       |   -
3   D0      | 37 (BCM 26)   |   -
4   CH0     | -             |   A0(connected with 1K ohm resistor)

__________________________________________________________________

    MCP3008 | RPI           |   MQ-2
1   CH0     |   -           |   A0(connected with 1K ohm resistor)
2   CH1     |   -           |   -
3   CH2     |   -           |   -
4   CH3     |   -           |   -
5   CH4     |   -           |   -
6   CH5     |   -           |   -
7   CH6     |   -           |   -
8   CH7     |   -           |   -
9   DGND    | 20(GND)       |   -
10  CS      | 24(SPI0 CE0)  |   -
11  DIN     | 19(SPI0 MOSI) |   -
12  DOUT    | 21(SPI0 MISO) |   -
13  CLK     | 23(SPI0 SCLK) |   -
14  AGND    | 20(GND)       |   -
15  VREF    | 9 (3.3V)      |   -
16  VCC     | 9 (3.3V)      |   -

Description:
MQ-2 - LPG(95% Methane), CO, CO2 sensor
    D0 - digital signal - D0 pin is set high by sensor to alert alarm - too much gas in the air (set threshold level using a screwdriver :) )
    A0 - returns analog signal that MUST be converted with an AC/DC because raspberry does not understand analogs.
       - Signal is 5V because MQ-2 uses 5V, so 1k OHm resistor is inserted to cut down voltage down to 3.3V so Raspberry SPI pins are not damaged :)
MCP3008 - AC/DC converter
    SPI - translates input analog signal to SPI interface (so raspberry can communicate)
        - All pins must be connected properly in /boot/config.txt file
            - dtparam=spi=on
              dtoverlay=spi0-1cs
in "mq" module the 'curve' value has been calibrated properly to my current city (Wrocław) average indoor air pollution (Methane ~1.7ppm, CO ~3ppm, CO2 ~400ppm)
'''
import time
from transmitter.sensors.modules.mq import MQ
from transmitter.sensors.sensor import Sensor
from observers.observable import Observable, Observer

class Gas_sensor(Sensor):
    def __init__(self, observers: Observable=None):
        Sensor.__init__(self)
        self.name = 'GAS'
        self.running = True
        self.topic = f'/{self.name}'
        self.sensor_id = self.name
        self.location = 'Wrocław'

        # Init Device
        self.dev = MQ(analogPin=0, observers=observers)

    def get_sensor_data(self):
        try:
            time.sleep(1.0)
            perc = self.dev.MQPercentage()
            if perc['CO'] and perc['CO2'] and perc['LPG']:
                return [
                    ('LPG', float(perc['LPG'])),
                    ('CO',  float(perc['CO'])),
                    ('CO2', float(perc['CO2']))
                ]
        except RuntimeError as error:
            print(error.args[0])
        except Exception as error:
            self.dev.exit()
            raise error
