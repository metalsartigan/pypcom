from .structure import DatatableStructure
from ..binary_command import BinaryCommand


class ReadDatatable(BinaryCommand):
    def __init__(self, *, structure: DatatableStructure, start_row_index: int = 0, row_count: int = 0, start_column_index: int = 0, column_count: int = 0, plc_id: int = 0):
        """Read a number of rows in a datatable and return the result in a list.

        :param structure: a DatatableStructure object defining the structure of the table to be read.
        :param start_row_index: The index of the first row to read. Defaults: 0
        :param row_count: The number of rows to read. 0 will read until the end of the table. Default: 0
        :param plc_id: The ID of the PLC. Default: 0
        :param start_column_index: Index of the first column to read. Default: 0
        :param column_count: The number of columns to read. 0 will read until the last column. Default: 0
        """
        super().__init__(command_number=4, plc_id=plc_id)
        self._table_structure = structure
        self._start_row_index = start_row_index
        self._row_count = row_count
        self._start_column_index = start_column_index
        self._column_count = column_count

    def _get_command_args(self):
        offset = self._table_structure.get_cell_offset(self._start_row_index, self._start_column_index)
        args = self._to_long_little_endian(offset)
        args.extend([0, 0])  # bytes 18 and 19 are not used.
        return args

    def _get_command_details(self):
        data_size = self._table_structure.get_row_size(self._start_column_index, self._column_count)
        details = self._to_little_endian(data_size)
        details.extend(self._to_little_endian(self._row_count))
        row_size = self._table_structure.get_row_size()
        details.extend(self._to_long_little_endian(row_size))
        details.extend([0] * 24)
        return details

    def parse_reply(self, buffer: bytearray):
        reply = super().parse_reply(buffer)
        return self._table_structure.parse_reply(reply, self._start_column_index, self._column_count)
