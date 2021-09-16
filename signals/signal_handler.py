import signal
import logging

class SIGINT_handler():
    def __init__(self):
        self.SIGINT = False
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        logging.info('SIGNAL_HANDLER: SIGINT catched. You pressed CONTROL + C !')
        self.SIGINT = True

signal_handler = SIGINT_handler()
