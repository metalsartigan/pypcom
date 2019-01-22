"""ASCII format enable read and write operations to registers and RTC, but
does not allow operations on datatables"""
from pcom.errors import PComError
from .base_command import BaseCommand, PROTOCOL_ASCII


class AsciiCommand(BaseCommand):
    def __init__(self, *, plc_id: int = 0, code: str, parameters: str = ''):
        super().__init__(plc_id=plc_id, protocol=PROTOCOL_ASCII)
        self.code = code
        self._parameters = parameters

    def get_bytes(self):
        frame = bytearray([0x2f])
        msg = '%02d%s%s' % (self._plc_id, self.code, self._parameters)
        frame.extend(msg.encode())
        frame.extend(self._get_crc_bytes(msg))
        frame.append(0xd)
        return frame

    def _get_crc_bytes(self, data):
        crc = sum(c.encode()[0] for c in data) % 256
        hex_str = hex(crc)[2:]
        hex_str = hex_str.zfill(2)
        return hex_str.upper().encode()

    def parse_reply(self, buffer: bytearray):
        buffer = super().parse_reply(buffer)
        return buffer[6:-3]

    def _validate_reply(self, buffer: bytearray):
        self.__validate_stx(buffer)
        self.__validate_plc_id(buffer)
        self.__validate_command_code(buffer)
        self.__validate_etx(buffer)
        self.__validate_crc(buffer)

    def __validate_stx(self, buffer: bytearray):
        expected = bytearray('/A'.encode())
        if buffer[:2] != expected:
            raise PComError("Invalid STX in reply. Expected: '%s', got: '%s'" % (expected, buffer[:2]), buffer)

    def __validate_plc_id(self, buffer: bytearray):
        expected = bytearray(('%02d' % self._plc_id).encode())
        if buffer[2:4] != expected:
            raise PComError("Invalid PLC ID in reply. Expected: '%s', got: '%s'" % (expected, buffer[2:4]), buffer)

    def __validate_command_code(self, buffer: bytearray):
        expected = bytearray(self.code.encode())
        if buffer[4:6] != expected:
            raise PComError("Invalid Command Code in reply. Expected: '%s', got: '%s'" % (expected, buffer[4:6]), buffer)

    def __validate_etx(self, buffer: bytearray):
        if buffer[-1] != 0xd:
            raise PComError("Invalid ETX in reply. Expected: '%s', got: '%s'" % (0xd, buffer[-1]), buffer)

    def __validate_crc(self, buffer: bytearray):
        actual = buffer[-3:-1]
        data = buffer[2:-3].decode()
        expected = self._get_crc_bytes(data)
        if actual != expected:
            raise PComError("Invalid CRC in reply. Expected: '%s', got: '%s'" % (expected, actual), buffer)
