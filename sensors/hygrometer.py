'''
DHT11 hygrometer & thermometer module.
'''
from threading import *

class Hygrometer(Thread):
    def __init__(self):
        super().__init__()
        self.name = 'HYG'
        self.running = True

    def run(self):
        print('run hygrometer')
        print(super().name)
