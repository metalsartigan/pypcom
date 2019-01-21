from .ascii_command import AsciiCommand

from datetime import datetime


class ReadRtc(AsciiCommand):
    def __init__(self, plc_id: int = 0):
        super().__init__(plc_id=plc_id, code='RC')

    def parse_reply(self, buffer: bytearray):
        buffer = super().parse_reply(buffer).decode()
        return datetime.strptime(buffer, '%S%M%H0%w%d%m%y')
