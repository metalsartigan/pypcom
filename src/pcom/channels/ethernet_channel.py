import socket

from .base_channel import BaseChannel


class EthernetChannel(BaseChannel):
    def __init__(self, *, address: tuple, timeout: int):
        self._address = address
        self._timeout = timeout
        self._socket = socket.socket()

    def open(self):
        # TODO: timeout
        self._socket.connect(self._address)

    def send(self, buffer: bytearray):
        self._socket.send(buffer)

    def close(self):
        self._socket.close()

    def receive(self):
        return self._socket.recv(4096)
