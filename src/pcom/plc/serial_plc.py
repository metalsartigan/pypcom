from pcom.commands.base_command import BaseCommand
from pcom.plc.base_plc import BasePlc


class SerialPlc(BasePlc):
    def _send_bytes(self, buffer: bytearray) -> None:
        raise NotImplementedError()

    def _receive_bytes(self) -> None:
        raise NotImplementedError()

    def send(self, command: BaseCommand) -> bytearray:
        raise NotImplementedError()
