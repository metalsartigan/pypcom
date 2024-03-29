from abc import ABC, abstractmethod
from typing import Any

PROTOCOL_ASCII = 101
PROTOCOL_BINARY = 102


class BaseCommand(ABC):
    def __init__(self, *, protocol, plc_id=0):
        self._plc_id = plc_id
        self.protocol = protocol

    @abstractmethod
    def get_bytes(self) -> bytearray:  # pragma: nocover
        pass

    def parse_reply(self, buffer: bytearray) -> bytearray:
        self._validate_reply(buffer)
        return buffer

    @abstractmethod
    def _validate_reply(self, buffer: bytearray) -> None:  # pragma: nocover
        pass
