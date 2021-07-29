'''
NAME barometer module.
'''
from threading import *

class Barometer(Thread):
    def __init__(self):
        super().__init__()
        self.name = 'BAR'
        self.running = True

    def run(self):
        print('run hygrometer')
        print(super().name)