import struct

from pcom.commands.ascii_command import AsciiCommand
from typing import List


class WriteFloats(AsciiCommand):
    def __init__(self, *, address: int, values: List[float] = [], plc_id: int = 0):
        self._validate_values(values)
        parameters = hex(address)[2:].upper().zfill(4)
        parameters += hex(len(values))[2:].upper().zfill(2)
        hex_bytes = [hex(b)[2:].upper().zfill(2) for b in self._pack_float_bytes(values)]
        parameters += ''.join(hex_bytes)
        super().__init__(plc_id=plc_id, code='SNF', parameters=parameters, reply_code='SN')

    def _validate_values(self, values: List[float]) -> None:
        if not all(-1.18e+38 <= v <= 3.4e+38 for v in values):
            raise ValueError("Float values must be between -1.18e+38 and 3.4e+38.")

    def _pack_float_bytes(self, values: List[float]) -> List[int]:
        buffer = bytearray()
        for value in values:
            packed_bytes = struct.pack('>f', value)
            ieee754 = packed_bytes[2:4] + packed_bytes[:2]
            buffer += ieee754
        return list(buffer)
