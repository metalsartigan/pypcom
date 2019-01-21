from collections import deque

from .operand_request import OperandRequest, OneBitRequest
from .binary_command import BinaryCommand


class ReadOperands(BinaryCommand):
    def __init__(self, *, plc_id: int = 0):
        self._requests = []
        super().__init__(command_number=77, plc_id=plc_id)

    def add_request(self, request: OperandRequest):
        self._requests.append(request)

    def _get_command_args(self):
        command_args = [0x0, 0x0, 0x0, 0x0]
        command_args += self._to_little_endian(len(self._requests))
        return command_args

    def _get_command_details(self):
        details = []
        self._requests.sort(key=lambda r: r.sequence)
        for request in self._requests:
            frame = []
            if request.length > 1:
                frame += self._to_little_endian(request.length)
            else:
                frame += self._to_little_endian(len(request.addresses))
            if len(request.addresses) == 1 and request.length > 1:
                frame += [request.code | 0x80, 0xff]
            else:
                frame += [request.code, 0xff]
            for a in request.addresses:
                frame += self._to_little_endian(a)
            details += frame
        return details

    def parse_reply(self, buffer: bytearray):
        self._requests.sort(key=lambda r: r.sequence)
        details = deque(super().parse_reply(buffer))
        self.__parse_binary_replies(details)
        self.__parse_other_replies(details)
        return self._requests

    def __parse_binary_replies(self, details: deque):
        binary_requests = [r for r in self._requests if isinstance(r, OneBitRequest)]
        binary_values = deque(OneBitRequest.parse_binary_values(binary_requests, details))
        for request in binary_requests:
            request.pop_values(binary_values)

    def __parse_other_replies(self, details: deque):
        other_requests = [r for r in self._requests if not isinstance(r, OneBitRequest)]
        for request in other_requests:
            request.pop_values(details)
