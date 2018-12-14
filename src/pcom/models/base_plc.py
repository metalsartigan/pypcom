from abc import ABC, abstractmethod


class BasePlc(ABC):
    def __init__(self, *, plc_id):
        self._plc_id = plc_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @abstractmethod
    def send(self, command):
        pass

    def close(self):
        pass
