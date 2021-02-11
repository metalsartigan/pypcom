import abc
import struct

from collections import deque
from datetime import timedelta
from typing import Any, List


def _chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


class DataType(abc.ABC):
    """Data types for datatables."""

    def __init__(self, size):
        self._size = size

    @property
    def size(self): return self._size

    @abc.abstractmethod
    def parse_value(self, data: List[int]):  # pragma: nocover
        pass

    @abc.abstractmethod
    def get_data_for_details(self, values: Any):  # pragma: nocover
        pass

    def _get_data_for_details(self, format: str, values: Any):
        buffer = bytearray()
        for value in values:
            buffer += struct.pack(format, value)
        return list(buffer)

    @abc.abstractmethod
    def validate_values(self, values: Any):  # pragma: nocover
        pass


class Bool(DataType):
    def __init__(self, number_of_elements: int = 1):
        self._number_of_elements = number_of_elements
        nb_fully_used_bytes = number_of_elements // 8
        nb_partially_used_bytes = min(1, number_of_elements % 8) if number_of_elements >= 8 else 1
        size = nb_fully_used_bytes + nb_partially_used_bytes
        super().__init__(size)

    def parse_value(self, data: List[int]):
        values = []
        for i in range(self._number_of_elements):
            number_index = i // 8
            value = (data[number_index] >> (i % 8)) & 0x01
            values.append(bool(value))
        return values

    def get_data_for_details(self, values: List[bool]):
        buffer = []
        boolean_bytes = _chunks(values, 8)
        for boolean_byte in boolean_bytes:
            byte = 0x00
            for i in range(len(boolean_byte)):
                if boolean_byte[i]:
                    byte |= 0x01 << i
            buffer.append(byte)
        return buffer

    def validate_values(self, values: List[bool]):
        if not all(type(v) is bool for v in values):
            raise ValueError("Values for Bool column must be booleans. Values: %s" % values)
        if len(values) != self._number_of_elements:
            raise ValueError("Values for Bool column do not match its structure. Column size: %d, values: %s" % (
                self._number_of_elements, values))


class String(DataType):
    def __init__(self, nb_chars: int):
        if nb_chars <= 0:
            raise ValueError("nb_chars parameter must be 1 or more.")
        super().__init__(nb_chars)

    def parse_value(self, data: List[int]):
        return ''.join(chr(v) for v in data)

    def get_data_for_details(self, values: str):
        return [ord(c) for c in values]

    def validate_values(self, values: str):
        if type(values) is not str:
            raise ValueError("Values for String column must be a string. Value: %s" % values)
        if len(values) != self._size:
            raise ValueError("Values for String column do not match its structure. Column size: %d, values: %s" % (
                self._size, values))


class Byte(DataType):
    def __init__(self, number_of_elements: int = 1):
        super().__init__(number_of_elements)

    def parse_value(self, data: List[int]):
        return [int(d) for d in data]

    def get_data_for_details(self, values: List[int]):
        return values

    def validate_values(self, values: List[int]):
        if any(type(v) is not int for v in values):
            raise ValueError("Values for Byte column must be numeric. Values: %s" % values)
        if len(values) != self._size:
            raise ValueError(
                "Values for Byte column do not match its structure. Column size: %d, values: %s" % (self._size, values))
        if not all(0 <= v <= 255 for v in values):
            raise ValueError("Byte values must be between 0 and 255. Values: %s" % values)


class UInt(DataType):
    def __init__(self, number_of_elements: int = 1):
        super().__init__(number_of_elements * 2)

    def parse_value(self, data: List[int]):
        return [struct.unpack('<H', bytes(c))[0] for c in _chunks(data, 2)]

    def get_data_for_details(self, values: List[int]):
        return self._get_data_for_details('<H', values)

    def validate_values(self, values: List[int]):
        if any(type(v) is not int for v in values):
            raise ValueError("Values for Unsigned Integer column must be numeric. Values: %s" % values)
        if len(values) != self._size / 2:
            raise ValueError("Values for Unsigned Integer do not match its structure. Column size: %d, values: %s" % (
                self._size / 2, values))
        if not all(0 <= v <= 65535 for v in values):
            raise ValueError("Unsigned Integer values must be between 0 and 65535.")


class Int(UInt):
    def parse_value(self, data: List[int]):
        return [struct.unpack('<h', bytes(c))[0] for c in _chunks(data, 2)]

    def get_data_for_details(self, values: List[int]):
        return self._get_data_for_details('<h', values)

    def validate_values(self, values: List[int]):
        if any(type(v) is not int for v in values):
            raise ValueError("Values for Integer column must be numeric. Values: %s" % values)
        if len(values) != self._size / 2:
            raise ValueError(
                "Values for Integer do not match its structure. Column size: %d, values: %s" % (self._size / 2, values))
        if not all(-32768 <= v <= 32767 for v in values):
            raise ValueError("Integer values must be between -32768 and 32767.")


class ULong(DataType):
    def __init__(self, number_of_elements: int = 1):
        super().__init__(number_of_elements * 4)

    def parse_value(self, data: List[int]):
        return [struct.unpack('<I', bytes(c))[0] for c in _chunks(data, 4)]

    def get_data_for_details(self, values: List[int]):
        return self._get_data_for_details('<I', values)

    def validate_values(self, values: List[int]):
        if any(type(v) is not int for v in values):
            raise ValueError("Values for Unsigned Long column must be numeric. Values: %s" % values)
        if len(values) != self._size / 4:
            raise ValueError("Values for Unsigned Long do not match its structure. Column size: %d, values: %s" % (
                self._size / 4, values))
        if not all(0 <= v <= 4294967295 for v in values):
            raise ValueError("Unsigned Long values must be between 0 and 4294967295.")


class Long(ULong):
    def parse_value(self, data: List[int]):
        return [struct.unpack('<i', bytes(c))[0] for c in _chunks(data, 4)]

    def get_data_for_details(self, values: List[int]):
        return self._get_data_for_details('<i', values)

    def validate_values(self, values: List[int]):
        if any(type(v) is not int for v in values):
            raise ValueError("Values for Long column must be numeric. Values: %s" % values)
        if len(values) != self._size / 4:
            raise ValueError(
                "Values for Long do not match its structure. Column size: %d, values: %s" % (self._size / 4, values))
        if not all(-2147483648 <= v <= 2147483647 for v in values):
            raise ValueError("Long values must be between -2147483648 and 2147483647.")


class Float(DataType):
    def __init__(self, number_of_elements: int = 1):
        super().__init__(number_of_elements * 4)

    def parse_value(self, data: List[int]):
        return [struct.unpack('<f', bytes(c[2:] + c[:2]))[0] for c in _chunks(data, 4)]

    def get_data_for_details(self, values: List[float]):
        buffer = bytearray()
        for value in values:
            bytes = struct.pack('<f', value)
            buffer += bytes[2:] + bytes[:2]
        return list(buffer)

    def validate_values(self, values: List[int]):
        if any(type(v) not in (int, float) for v in values):
            raise ValueError("Values for Float column must be numeric. Values: %s" % values)
        if len(values) != self._size / 4:
            raise ValueError(
                "Values for Float do not match its structure. Column size: %d, values: %s" % (self._size / 4, values))
        if not all(-3.4e+38 <= v <= 3.4e+38 for v in values):
            raise ValueError("Float values must be between 1.18e-38 and 3.4e+38.")


class Timer(DataType):
    # https://forum.unitronics.com/topic/7631-how-to-read-a-timer-column-in-a-datatable/
    def __init__(self, number_of_elements: int = 1):
        super().__init__(number_of_elements * 12)

    def parse_value(self, data: List[int]):
        chunks = [c[2:-6] for c in _chunks(data, 12)]
        numeric_values = [struct.unpack('<i', bytes(c))[0] for c in chunks]
        return [timedelta(milliseconds=n * 10) for n in numeric_values]

    def get_data_for_details(self, values: List[timedelta]):
        details = [int(delta / timedelta(milliseconds=10)) for delta in values]
        data = []
        for detail in details:
            data.extend([0] * 2)  # unused bytes
            data.extend(self._get_data_for_details('<i', [detail]))
            data.extend([0] * 6)  # unused bytes
        return data

    def validate_values(self, values: List[timedelta]):
        if any(type(v) is not timedelta for v in values):
            raise ValueError("Values for Timer column must be timedelta. Values: %s" % values)
        if any(v > timedelta(hours=99, minutes=59, seconds=59, milliseconds=990) for v in values):
            raise ValueError(
                "Values of timedelta for Timer column must not exceed 99 hours, 59 minutes, 59 seconds and 990 milliseconds. Values: %s" % values)
        if len(values) != self._size / 12:
            raise ValueError(
                "Values for Timer do not match its structure. Column size: %d, values: %s" % (self._size, values))


class DatatableStructure:
    def __init__(self, name: str, *, offset: int, rows: int, columns: List[DataType]):
        self._name = name
        self._offset = offset
        self._columns = columns
        self._rows = rows

    @property
    def name(self): return self._name
    @property
    def offset(self): return self._offset
    @property
    def columns(self): return list(self._columns)
    @property
    def rows(self): return self._rows

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

    def get_row_count(self, start_row_index: int, row_count: int):
        """Computes the number of rows.

        :param start_row_index: The first row.
        :param row_count: The number of rows. 0 will include all remaining rows.
        :return: An integer representing the number of rows that can be read.
        """
        if start_row_index < 0:
            raise ValueError("Invalid start_index: %d" % start_row_index)
        if row_count < 0:
            raise ValueError("Invalid count: %d" % row_count)

        if start_row_index + row_count > self._rows or start_row_index == self._rows:
            msg = "start_index and count exceed the number of rows: %d, %d" % (start_row_index, row_count)
            raise ValueError(msg)
        if row_count == 0:
            row_count = self._rows - start_row_index

        return row_count

    def parse_reply(self, reply: List[int], start_column_index: int, column_count: int):
        if column_count == 0:
            column_count = len(self._columns) - start_column_index

        reply_rows = self._split_reply_into_raw_rows(reply, start_column_index, column_count)
        return [self._parse_result_row(row, start_column_index, column_count) for row in reply_rows]

    def _split_reply_into_raw_rows(self, reply, start_column_index, column_count):
        row_size = self.get_row_size(start_column_index, column_count)
        return _chunks(reply, row_size)

    def _parse_result_row(self, raw_row, start_column_index, column_count):
        row_queue = deque(raw_row)
        row = []
        for column in self._columns[start_column_index:start_column_index + column_count]:
            column_data = [row_queue.popleft() for _ in range(column.size)]
            column_value = column.parse_value(column_data)
            row.append(column_value)
        return row

    def validate_row_values(self, row_values: List[list], *, start_column_index: int):
        if not 0 <= start_column_index <= (len(self._columns) - 1):
            raise ValueError("Invalid start_column_index: %d" % start_column_index)
        actual, expected = len(row_values), len(self._columns) - start_column_index
        if actual == 0:
            raise ValueError("Row has no value, expected %d." % expected)
        if actual > expected:
            raise ValueError(
                "The number of values in row exceeds what is expected. Expected %d, got %d." % (actual, expected))
        for i, column_values in enumerate(row_values):
            self._columns[start_column_index + i].validate_values(column_values)

    def get_row_data_for_details(self, row_values: List[list], *, start_column_index: int):
        if not 0 <= start_column_index <= (len(self._columns) - 1):
            raise ValueError("Invalid start_column_index: %d" % start_column_index)
        buffer = []
        for i, column_values in enumerate(row_values):
            buffer.extend(self._columns[start_column_index + i].get_data_for_details(column_values))
        return buffer
