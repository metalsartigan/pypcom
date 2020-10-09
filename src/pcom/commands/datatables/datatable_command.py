from abc import ABC

from ..binary_command import BinaryCommand
from .structure import DatatableStructure


class DatatableCommand(BinaryCommand, ABC):
    def __init__(self, command_number: int, structure: DatatableStructure, start_row_index: int, row_count: int,
                 start_column_index: int, column_count: int, plc_id: int):
        super().__init__(command_number=command_number, plc_id=plc_id)
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
