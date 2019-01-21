from pcom.commands.ascii_command import AsciiCommand


class MockAsciiCommand(AsciiCommand):
    def __init__(self, arg1: int = 1, *, kwarg1: int = 2, plc_id: int = 0):
        super().__init__(plc_id=plc_id, code='MK')
        self.arg1 = arg1
        self.kwarg1 = kwarg1
        self._bytes = bytearray([1, 2, 3, 4])

    def set_bytes(self, value):
        self._bytes = value

    def get_bytes(self):
        return self._bytes

    def get_ethernet_recv_bytes(self):
        return bytearray(b'\x1fhe\x00\x12\x00/A00MK\x02\x03\x0401\r')

    def get_recv_bytes(self):
        return bytearray(b'/A00MK\x02\x03\x0401\r')

    def get_crc_bytes(self, data):
        return self._get_crc_bytes(data)
