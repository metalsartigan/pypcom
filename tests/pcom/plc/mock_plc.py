from pcom.plc.base_plc import BasePlc


class MockPlc(BasePlc):
    def __init__(self):
        super().__init__()

    def _send_bytes(self, buffer: bytearray):
        pass

    def _receive_bytes(self):
        pass

