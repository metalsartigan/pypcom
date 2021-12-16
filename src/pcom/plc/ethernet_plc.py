import errno
import os
import socket
from typing import Tuple, Any

from pcom.commands.base_command import BaseCommand, PROTOCOL_ASCII, PROTOCOL_BINARY
from pcom.errors import PComError
from .base_plc import BasePlc
from pcom.plc.ethernet_command_wrapper import EthernetCommandWrapper


class EthernetPlc(BasePlc):
    def __init__(self, *, address: Tuple[str, int], timeout: int = 5):
        super().__init__()
        self._address = address
        self._timeout = timeout
        self._socket: socket.socket or None = None
        self._buffer = bytearray()

    @property
    def is_connected(self) -> bool:
        return bool(self._socket)

    @property
    def address(self) -> Tuple[str, int]:
        return self._address

    def connect(self) -> None:
        self._socket = socket.socket()
        self._socket.settimeout(self._timeout)
        try:
            self._socket.connect(self._address)
        except (TimeoutError, socket.timeout, ConnectionRefusedError) as ex:
            self.close()
            raise PComError(str(ex))
        except OSError as ex:
            self.close()
            if ex.errno == errno.EHOSTUNREACH:
                raise PComError(os.strerror(ex.errno))
            else:
                raise

    def close(self) -> None:
        self._buffer.clear()
        if self._socket:
            self._socket.close()
            self._socket = None

    def send(self, command: BaseCommand) -> Any:
        if not self._socket:
            raise PComError("Cannot send while not connected.")
        command = EthernetCommandWrapper(command)
        return super().send(command)

    def _send_bytes(self, buffer: bytearray) -> None:  # pragma: nocover
        self._socket.send(buffer)

    def _socket_recv(self) -> bytearray:  # pragma: nocover
        return self._socket.recv(4096)

    def _receive_bytes(self) -> bytearray:
        try:
            header = None
            while True:
                if len(self._buffer) - 1 >= 2 and self._buffer[2] in (PROTOCOL_ASCII, PROTOCOL_BINARY):
                    header = self._buffer[:6]
                    if len(header) == 6:
                        transaction_size = header[5] << 8 | header[4]
                        end = 6 + transaction_size
                        transaction = self._buffer[:end]
                        if len(transaction) == transaction_size:
                            del self._buffer[:end]
                            return transaction
                elif self._buffer:
                    del self._buffer[0]
                if len(self._buffer) <= 2 or header:
                    self._buffer.extend(self._socket_recv())

        except socket.timeout as ex:
            raise PComError(str(ex))
