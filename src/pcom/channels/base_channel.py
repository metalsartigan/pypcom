from abc import ABC, abstractmethod


class BaseChannel(ABC):
    @abstractmethod
    def open(self):
        pass

    def close(self):
        pass

    @abstractmethod
    def send(self, buffer: bytearray):
        pass

    @abstractmethod
    def receive(self):
        pass
