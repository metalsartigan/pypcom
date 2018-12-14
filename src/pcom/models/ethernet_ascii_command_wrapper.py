import random


class EthernetAsciiCommandWrapper:
    def __init__(self, base_command):
        super().__init__()
        self._base_command = base_command

    def get_bytes(self):
        base_command_bytes = self._base_command.get_bytes()
        header = [random.randint(0, 128), random.randint(0, 128)]
        header.extend([101, 0, len(base_command_bytes), 0])
        frame = bytearray(header)
        frame.extend(base_command_bytes)
        return frame
