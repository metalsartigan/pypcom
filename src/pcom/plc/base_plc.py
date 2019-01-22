from abc import ABC, abstractmethod

from pcom.commands.base_command import BaseCommand
from pcom.errors import PComError


class BasePlc(ABC):
    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()

    def send(self, command: BaseCommand):
        send_buffer = command.get_bytes()
        if len(send_buffer) > 500:
            raise PComError('The PLC cannot accept messages that are longer than 500 bytes.', send_buffer)
        self._send_bytes(send_buffer)
        buffer = self._receive_bytes()
        return command.parse_reply(buffer)

    @abstractmethod
    def _send_bytes(self, buffer: bytearray):  # pragma: nocover
        pass

    @abstractmethod
    def _receive_bytes(self):  # pragma: nocover
        pass

    def _connect(self):
        pass

    def _close(self):
        pass
