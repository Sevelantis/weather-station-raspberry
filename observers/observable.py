from enum import Enum

class ObserversList(Enum):
    PUBLISHER = 'PUB'
    LOGGER = 'LOG'

class Observer:
    def __init__(self, name) -> None:
        self.name = name
        self.observers = []

    def notify(data) -> None:
        pass

class Observable:
    def __init__(self) -> None:
        self.observers = []

    def add_observer(self, observer: Observer) -> None:
        if observer not in self.observers:
            self.observers.append(observer)

    def notify_observers(self, data) -> None:
        for observer in self.observers:
            observer.notify(data)

    def notify_observer(self, data, name) -> None:
        for observer in self.observers:
            if observer.name == name:
                observer.notify(data)
