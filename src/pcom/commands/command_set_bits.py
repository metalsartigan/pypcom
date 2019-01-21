from .ascii_command import AsciiCommand


class CommandSetBits(AsciiCommand):
    OUTPUT = 'SA'
    MEMORY = 'SB'
    SYSTEM = 'SS'

    def __init__(self, *, code: str, address: int, values: list = [], plc_id: int = 0):
        parameters = hex(address)[2:].zfill(4)
        parameters += hex(len(values))[2:].zfill(2)
        parameters += ''.join('1' if v else '0' for v in values)
        super().__init__(plc_id=plc_id, code=code, parameters=parameters)

    def parse_reply(self, buffer: bytearray):
        buffer = super().parse_reply(buffer).decode()
        return buffer == ''
