from .base_plc import BasePlc
from pcom.channels import EthernetChannel
from pcom.models import AsciiCommand, EthernetAsciiCommandWrapper


class EthernetPcomPlc(BasePlc):
    def __init__(self, *, address, timeout=0, plc_id=0):
        super().__init__(plc_id=plc_id)
        self._address = address
        self._timeout = timeout
        self._channel = None

    def connect(self):
        self._channel = EthernetChannel(address=self._address, timeout=self._timeout)
        self._channel.open()

    def close(self):
        if self._channel:
            self._channel.close()
            self._channel = None

    def send(self, command):
        if self._channel:
            command.set_plc_id(self._plc_id)
            if isinstance(command, AsciiCommand):
                command = EthernetAsciiCommandWrapper(command)
            self._channel.send(command.get_bytes())
            # TODO: return real data object
            return self._channel.receive()
