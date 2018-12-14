"""ASCII format enable read and write operations to registers and RTC, but
does not allow operations on datatables"""

from .base_command import BaseCommand


class AsciiCommand(BaseCommand):
    def __init__(self, *, code, parameters=''):
        super().__init__()
        self._code = code
        self._parameters = parameters

    def _get_crc_bytes(self, data):
        crc = sum(c.encode()[0] for c in data) % 256
        hex_str = hex(crc)[2:]
        return hex_str.upper().encode()

    def get_bytes(self):
        frame = bytearray([0x2f])
        msg = '%02d%s%s' % (self._plc_id, self._code, self._parameters)
        frame.extend(msg.encode())
        frame.extend(self._get_crc_bytes(msg))
        frame.append(0xd)
        return frame
