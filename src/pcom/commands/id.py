from .ascii_command import AsciiCommand


class ID(AsciiCommand):
    def __init__(self, plc_id: int = 0):
        super().__init__(plc_id=plc_id, code='ID')
