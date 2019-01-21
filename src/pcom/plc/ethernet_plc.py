import errno
import os
import socket

from pcom.commands.base_command import BaseCommand, PROTOCOL_ASCII, PROTOCOL_BINARY
from pcom.errors import PComError
from .base_plc import BasePlc
from pcom.plc.ethernet_command_wrapper import EthernetCommandWrapper


class EthernetPlc(BasePlc):
    def __init__(self, *, address: tuple, timeout: int = 5):
        super().__init__()
        self._address = address
        self._timeout = timeout
        self._socket = socket.socket()
        self._buffer = bytearray()

    def _connect(self):
        self._socket.settimeout(self._timeout)
        try:
            self._socket.connect(self._address)
        except (TimeoutError, socket.timeout, ConnectionRefusedError) as ex:
            raise PComError(str(ex))
        except OSError as ex:
            if ex.errno == errno.EHOSTUNREACH:
                raise PComError(os.strerror(ex.errno))
            else:
                raise

    def _close(self):
        self._socket.close()

    def send(self, command: BaseCommand):
        command = EthernetCommandWrapper(command)
        return super().send(command)

    def _send_bytes(self, buffer: bytearray):  # pragma: nocover
        self._socket.send(buffer)

    def _socket_recv(self):  # pragma: nocover
        return self._socket.recv(4096)

    def _receive_bytes(self):
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
