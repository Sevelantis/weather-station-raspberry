import signal
import logging

class SIGNAL_Handler():
    def __init__(self):
        self.SIGINT = False
        self.HARD_RESET = False
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        if self.SIGINT:
            logging.info('signal_handler: COMBO!!! COMTROL + C         x2!\n')
            exit()
        logging.info('signal_handler: SIGINT signal catched. You pressed CONTROL + C !')
        self.SIGINT = True

signal_handler = SIGNAL_Handler()
