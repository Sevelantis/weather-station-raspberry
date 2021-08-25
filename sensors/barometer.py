'''
NAME barometer module.
'''
from threading import *
from signal_handler import handler
import time

class Barometer(Thread):
    def __init__(self):
        super().__init__()
        self.name = 'BAR'
        self.running = True
    def run(self):
        while self.running:
            # print(super().name)

            self.read_data()

            if handler.SIGINT:
                self.running = False
                break
    
    def read_data(self):
        time.sleep(5.0)