"""Binary format enables read operation on registers, and read+write operations
on datatables."""

from abc import ABC, abstractmethod

from pcom.errors import PComError
from .base_command import BaseCommand, PROTOCOL_BINARY


class BinaryCommand(BaseCommand, ABC):
    def __init__(self, *, command_number: int, plc_id: int = 0):
        super().__init__(plc_id=plc_id, protocol=PROTOCOL_BINARY)
        self._command_number = command_number
        self._command_details = []
        self._stx = [0x2F, 0x5F, 0x4F, 0x50, 0x4C, 0x43]

    def get_bytes(self):
        details = self._get_command_details()
        return bytearray(self.__get_header(details) + details + self.__get_footer(details))

    def __get_header(self, details):
        header = self._stx + [self._plc_id, 0xfe, 0x1, 0x0, 0x0, 0x0, self._command_number, 0x0]
        header += self._get_command_args()[:6]
        header += self._to_little_endian(len(details))
        header += self._get_crc_bytes(header)
        return header

    def __get_footer(self, details):
        footer = self._get_crc_bytes(details)
        footer += '\\'.encode()
        return footer

    def _to_little_endian(self, word):
        return [word & 255, word >> 8]

    def _get_crc_bytes(self, data):
        val = ~(sum(data) % 0x10000) + 1
        val = val & 0xffff  # convert to unsigned value
        return self._to_little_endian(val)

    @abstractmethod
    def _get_command_args(self):  # pragma: nocover
        pass

    @abstractmethod
    def _get_command_details(self):  # pragma: nocover
        pass

    def parse_reply(self, buffer: bytearray):
        super().parse_reply(buffer)
        details = buffer[24:-3]
        return details

    def _validate_reply(self, buffer: bytearray):
        self.__validate_stx(buffer)
        self.__validate_canbus_id(buffer)
        self.__validate_command_number(buffer)
        self.__validate_data_length(buffer)
        self.__validate_header_crc(buffer)
        self.__validate_details_crc(buffer)
        self.__validate_etx(buffer)

    def __validate_stx(self, buffer: bytearray):
        if buffer[:6] != bytearray(self._stx):
            raise PComError("Invalid STX in reply. Expected: '%s', got: '%s'" % (bytearray(self._stx), buffer[:6]), buffer)

    def __validate_canbus_id(self, buffer: bytearray):
        if buffer[6:8] != bytearray([0xfe, self._plc_id]):
            raise PComError("Invalid plc id in reply. Expected: '%s', got: '%s'" % ([0xfe, self._plc_id], buffer[6:8]), buffer)

    def __validate_command_number(self, buffer: bytearray):
        expected = self._command_number + 0x80
        if buffer[12] != expected:
            raise PComError("Invalid command number in reply. Expected: '%s', got: '%s'" % (expected, buffer[12]), buffer)

    def __validate_data_length(self, buffer: bytearray):
        expected = buffer[20] | buffer[21] << 8
        actual = len(buffer[24:-3])
        if expected != actual:
            raise PComError("Invalid data length in reply. Expected: '%s', got: '%s'" % (expected, actual), buffer)

    def __validate_header_crc(self, buffer: bytearray):
        actual = bytearray(buffer[22:24])
        expected = bytearray(self._get_crc_bytes(buffer[:22]))
        if expected != actual:
            raise PComError("Invalid CRC in reply header. Expected: '%s', got: '%s'" % (expected, actual), buffer)

    def __validate_details_crc(self, buffer: bytearray):
        actual = bytearray(buffer[-3:-1])
        expected = bytearray(self._get_crc_bytes(buffer[24:-3]))
        if expected != actual:
            raise PComError("Invalid CRC in reply details. Expected: '%s', got: '%s'" % (expected, actual), buffer)

    def __validate_etx(self, buffer: bytearray):
        if buffer[-1] != 0x5c:
            raise PComError("Invalid ETX in reply. Expected: '%s', got: '%s'" % (0x5c, buffer[-1]), buffer)
