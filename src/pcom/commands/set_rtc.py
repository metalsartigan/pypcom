from .ascii_write_command import AsciiWriteCommand

from datetime import datetime


class SetRtc(AsciiWriteCommand):
    def __init__(self, *, value: datetime, plc_id: int = 0):
        parameters = datetime.strftime(value, '%S%M%H0%w%d%m%y')
        super().__init__(plc_id=plc_id, code='SC', parameters=parameters)
