import struct

from pcom.commands.ascii_command import AsciiCommand
from typing import Tuple, List


class WriteIntegers(AsciiCommand):
    # REGISTER_TYPE = (command_code, data_size)
    MI = ('SW', 2)
    ML = ('SNL', 4)
    DW = ('SND', 4)
    SI = ('SF', 2)
    SL = ('SNH', 4)
    SDW = ('SNJ', 4)
    # MF is handled by the WriteFloats class.

    def __init__(self, *, code: Tuple[str, int], address: int, values: List[int] = [], plc_id: int = 0):
        parameters = hex(address)[2:].upper().zfill(4)
        parameters += hex(len(values))[2:].upper().zfill(2)
        if code[1] == 2:
            values_bytes = self._pack_bytes('>h', values)
            reply_code = code[0]
        else:
            values_bytes = self._pack_bytes('>i', values)
            reply_code = code[0][:2]
        parameters += ''.join(hex(b)[2:].upper().zfill(2) for b in values_bytes)
        super().__init__(plc_id=plc_id, code=code[0], parameters=parameters, reply_code=reply_code)
