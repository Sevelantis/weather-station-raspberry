'''
NAME gas_sensor module.
'''
from threading import *

class Gas_sensor(Thread):
    def __init__(self):
        super().__init__()
        self.name = 'GAS'
        self.running = True

    def run(self):
        print('run gas_sensor')
        print(super().name)