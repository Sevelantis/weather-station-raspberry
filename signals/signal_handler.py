import signal
from observers.observable import Observable

class SIGINT_handler():
    def __init__(self):
        self.SIGINT = False
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        self.SIGINT = True

signal_handler = SIGINT_handler()
