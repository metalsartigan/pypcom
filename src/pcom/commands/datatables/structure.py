import abc
import struct

from collections import deque
from itertools import groupby
from typing import List


class DataType(abc.ABC):
    """Data types for datatables."""

    def __init__(self, size):
        self._size = size

    @property
    def size(self):
        return self._size

    @abc.abstractmethod
    def parse_value(self, data: List[int]):  # pragma: nocover
        raise NotImplemented()


class Bool(DataType):
    def __init__(self, size=1):
        super().__init__(size)

    @property
    def size(self):
        nb_fully_used_bytes = self._size // 8
        nb_partially_used_bytes = min(1, self._size % 8) if self._size >= 8 else 1
        return nb_fully_used_bytes + nb_partially_used_bytes

    def parse_value(self, data: List[int]):
        values = []
        for i in range(self._size):
            number_index = i // 8
            value = (data[number_index] >> (i % 8)) & 0x01
            values.append(bool(value))
        return values


class String(DataType):
    def __init__(self, nb_chars: int):
        if nb_chars <= 0:
            raise ValueError("nb_chars parameter must be 1 or more.")
        super().__init__(nb_chars)

    def parse_value(self, data: List[int]):
        return ''.join(chr(v) for v in data)


class Byte(DataType):
    def __init__(self):
        super().__init__(1)

    def parse_value(self, data: List[int]):
        return int(data[0])


class UInt(DataType):
    def __init__(self):
        super().__init__(2)

    def parse_value(self, data: List[int]):
        return struct.unpack('<H', bytes(data))[0]


class Int(UInt):
    def parse_value(self, data: List[int]):
        return struct.unpack('<h', bytes(data))[0]


class ULong(DataType):
    def __init__(self):
        super().__init__(4)

    def parse_value(self, data: List[int]):
        return struct.unpack('<I', bytes(data))[0]


class Long(ULong):
    def parse_value(self, data: List[int]):
        return struct.unpack('<i', bytes(data))[0]


class Float(DataType):
    def __init__(self):
        super().__init__(4)

    def parse_value(self, data: List[int]):
        buffer = bytes(data[2:] + data[:2])
        return struct.unpack('<f', buffer)[0]


class Timer(DataType):
    def __init__(self):
        super().__init__(12)

    def parse_value(self, data: List[int]):
        # There is no documentation on this type of column.
        # https://forum.unitronics.com/topic/7631-how-to-read-a-timer-column-in-a-datatable/
        return data


class DatatableStructure:
    def __init__(self, name: str, *, offset: int, rows: int, columns: List[DataType]):
        self._name = name
        self._offset = offset
        self._columns = columns
        self._rows = rows

    @property
    def name(self):
        return self._name

    @property
    def offset(self):
        return self._offset

    @property
    def columns(self):
        return list(self._columns)

    @property
    def rows(self):
        return self._rows

    def get_cell_offset(self, row_index: int, column_index: int):
        """Computes the absolute offset of a specific position.

        :param row_index: The index of the row in the table
        :param column_index: The index of the column in the table
        :return: An integer representing the absolute offset of the cell in memory.
        """
        if row_index < 0 or row_index >= self._rows:
            raise ValueError("Invalid row_index: %d" % row_index)
        if column_index < 0 or column_index >= len(self._columns):
            raise ValueError("Invalid column_index: %d" % column_index)
        row_size = self.get_row_size()
        row_offset = row_index * row_size
        column_offset = 0 if column_index == 0 else self.get_row_size(0, column_index)
        return self._offset + row_offset + column_offset

    def get_row_size(self, start_column_index: int = 0, column_count: int = 0):
        """Computes the size of the data for a group of columns.

        :param start_column_index: The first column. Default: 0
        :param column_count: The number of columns. 0 will include all the next columns.
        :return: An integer representing the total size.
        """
        if start_column_index < 0:
            raise ValueError("Invalid start_index: %d" % start_column_index)
        if column_count < 0:
            raise ValueError("Invalid count: %d" % column_count)
        if start_column_index + column_count > len(self._columns) or start_column_index == len(self._columns):
            msg = "start_index and count exceed the number of columns: %d, %d" % (start_column_index, column_count)
            raise ValueError(msg)
        if column_count == 0:
            column_count = len(self._columns)

        return sum(c.size for c in self._columns[start_column_index:start_column_index + column_count])

    def parse_reply(self, reply: List[int], start_column_index: int, column_count: int):
        if column_count == 0:
            column_count = len(self._columns) - start_column_index

        reply_rows = self._split_reply_into_raw_rows(reply, start_column_index, column_count)
        return [self._parse_result_row(row) for row in reply_rows]

    def _split_reply_into_raw_rows(self, reply, start_column_index, column_count):
        def chunks(l, n):
            n = max(1, n)
            return [l[i:i + n] for i in range(0, len(l), n)]

        row_size = self.get_row_size(start_column_index, column_count)
        return chunks(reply, row_size)

    def _parse_result_row(self, raw_row):
        row_queue = deque(raw_row)
        row = []
        for column in self._columns:
            column_data = [row_queue.popleft() for _ in range(column.size)]
            column_value = column.parse_value(column_data)
            row.append(column_value)
        return row
