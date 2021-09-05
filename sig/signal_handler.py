import sys
import signal

class SIGINT_handler():
    def __init__(self):
        self.SIGINT = False

    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        self.SIGINT = True

handler = SIGINT_handler()
signal.signal(signal.SIGINT, handler.signal_handler)
