'''
NAME thermometer module.
'''
from threading import *

class Thermometer(Thread):
    def __init__(self):
        super().__init__()
        self.name = 'THE'
        self.running = True

    def run(self):
        print('run thermometer')
        print(super().name)