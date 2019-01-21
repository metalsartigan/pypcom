from pcom.commands.binary_command import BinaryCommand


class MockBinaryCommand(BinaryCommand):
    def __init__(self, plc_id: int = 0):
        super().__init__(plc_id=plc_id, command_number=66)

    def _get_command_args(self):
        pass

    def _get_command_details(self):
        pass

    def get_bytes(self):
        return bytearray()

    def get_ethernet_recv_bytes(self):
        transaction = bytearray(b'/_OPLC\xFE') + bytearray([self._plc_id]) + bytearray(b'\x01\x00\x00\x00\xc2\x00\x01\x02\x03\x04\x05\x06\x04\x00\x6a\xfc\x10\x11\x02\x03\xda\xff\x5c')
        length = len(transaction)
        len_bytes = [(length & 0xff), length >> 8]
        return bytearray(b'\x1fhf\x00') + bytearray(len_bytes) + transaction

    def get_recv_bytes(self):
        return bytearray(b'\x02\x03\x04')
