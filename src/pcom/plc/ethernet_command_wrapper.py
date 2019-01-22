import random

from pcom.commands.base_command import BaseCommand
from pcom.errors import PComError


class EthernetCommandWrapper(BaseCommand):
    def __init__(self, base_command: BaseCommand):
        super().__init__(plc_id=base_command._plc_id, protocol=base_command.protocol)
        self.base_command = base_command
        self.command_id = self._create_command_id()

    def _create_command_id(self):
        return [random.randint(0, 99), random.randint(0, 99)]

    def get_bytes(self):
        frame = self.__get_header()
        base_command_bytes = self.base_command.get_bytes()
        frame.extend(base_command_bytes)
        return frame

    def __get_header(self):
        base_command_bytes = self.base_command.get_bytes()
        header = list(self.command_id)
        header.extend([self.base_command.protocol, 0, len(base_command_bytes), 0])
        return bytearray(header)

    def parse_reply(self, buffer: bytearray):
        super().parse_reply(buffer)
        command_buffer = buffer[6:]
        return self.base_command.parse_reply(command_buffer)

    def _validate_reply(self, buffer: bytearray):
        header = buffer[:6]
        header_bytes = self.__get_header()
        expected = header_bytes[:4]
        actual = header[:4]
        if actual != expected:
            raise PComError("Ethernet header mismatch. Expected: '%s' found: '%s'" % (expected, actual), buffer)
