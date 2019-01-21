from abc import ABC, abstractmethod
from collections import deque
import math
import struct


class OperandRequest(ABC):
    def __init__(self, *, sequence: int, code: int, addresses: list, length: int):
        self.code = code
        self.sequence = sequence
        self.addresses = addresses
        self.length = length
        self.values = []

    @abstractmethod
    def pop_values(self, buffer: deque):  # pragma: nocover
        pass

    def _get_values_count(self):
        return max(len(self.addresses), self.length)


class OneBitRequest(OperandRequest):
    def __init__(self, **kwargs):
        super().__init__(sequence=1, **kwargs)

    def pop_values(self, buffer: deque):
        for __ in range(self._get_values_count()):
            value = buffer.popleft()
            self.values.append(value)

    @classmethod
    def parse_binary_values(cls, instances: list, buffer: deque):
        count = sum(r._get_values_count() for r in instances)
        int_count = math.ceil(count / 16.0)
        bits = []
        for _ in range(int_count):
            byte1 = buffer.popleft()
            byte2 = buffer.popleft()
            value = byte1 | (byte2 << 8)
            bits.extend([b == '1' for b in bin(value)[2:].rjust(16)][-count:][::-1])  # convert, pad, last values, reverse
        return bits


class SixteenBitsRequest(OperandRequest):
    def __init__(self, **kwargs):
        super().__init__(sequence=2, **kwargs)

    def pop_values(self, buffer: deque):
        for _ in range(self._get_values_count()):
            byte1 = buffer.popleft()
            byte2 = buffer.popleft()
            value = byte1 | (byte2 << 8)
            self.values.append(value)


class ThirtytwoBitsRequest(OperandRequest):
    def __init__(self, **kwargs):
        super().__init__(sequence=3, **kwargs)

    def pop_values(self, buffer: deque):
        for _ in range(self._get_values_count()):
            bytes = bytearray()
            bytes.append(buffer.popleft())
            bytes.append(buffer.popleft())
            bytes.append(buffer.popleft())
            bytes.append(buffer.popleft())
            value = self._convert_bytes(bytes)
            self.values.append(value)

    def _convert_bytes(self, bytes: bytearray):
        return bytes[0] | (bytes[1] << 8) | (bytes[2] << 16) | (bytes[3] << 24)


class FloatRequest(ThirtytwoBitsRequest):
    def _convert_bytes(self, bytes: bytearray):
        ieee754 = bytes[2:4] + bytes[:2]
        return struct.unpack('f', ieee754)[0]


class MB(OneBitRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x01, addresses=addresses, length=length)


class SB(OneBitRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x02, addresses=addresses, length=length)


class MI(SixteenBitsRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x03, addresses=addresses, length=length)


class SI(SixteenBitsRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x04, addresses=addresses, length=length)


class ML(ThirtytwoBitsRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x05, addresses=addresses, length=length)


class SL(ThirtytwoBitsRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x06, addresses=addresses, length=length)


class MF(FloatRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x07, addresses=addresses, length=length)


class SF(FloatRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x08, addresses=addresses, length=length)


class Input(OneBitRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x09, addresses=addresses, length=length)


class Output(OneBitRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x0a, addresses=addresses, length=length)


class TimerRunBit(OneBitRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x0b, addresses=addresses, length=length)


class CounterRunBit(OneBitRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x0c, addresses=addresses, length=length)


class DW(ThirtytwoBitsRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x10, addresses=addresses, length=length)


class SDW(ThirtytwoBitsRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x11, addresses=addresses, length=length)


class CounterCurrent(SixteenBitsRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x12, addresses=addresses, length=length)


class CounterPreset(SixteenBitsRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x13, addresses=addresses, length=length)


class TimerCurrent(ThirtytwoBitsRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x14, addresses=addresses, length=length)


class TimerPreset(ThirtytwoBitsRequest):
    def __init__(self, *, addresses: list, length: int = 1):
        super().__init__(code=0x15, addresses=addresses, length=length)
