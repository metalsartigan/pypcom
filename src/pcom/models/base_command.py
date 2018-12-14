from abc import ABC, abstractmethod


class BaseCommand(ABC):
    def __init__(self):
        self._plc_id = 0

    @abstractmethod
    def get_bytes(self):
        pass

    def set_plc_id(self, value):
        self._plc_id = value
