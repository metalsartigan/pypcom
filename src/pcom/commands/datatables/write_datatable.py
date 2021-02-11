from .datatable_command import DatatableCommand
from .structure import DatatableStructure


class WriteDatatable(DatatableCommand):
    def __init__(self, *, structure: DatatableStructure, start_row_index: int = 0,
                 start_column_index: int = 0, plc_id: int = 0, data: list):
        """Writes a number of rows in a datatable."""
        self._validate_data(structure, data, start_column_index)
        self._data = data
        row_count = len(self._data)
        column_count = len(self._data[0])
        super().__init__(68, structure, start_row_index, row_count, start_column_index, column_count, plc_id)

    @property
    def data(self): return list(self._data)

    def _get_command_details(self):
        data_size = self._table_structure.get_row_size(self._start_column_index, self._column_count)
        details = self._to_little_endian(data_size)
        details.extend(self._to_little_endian(self._row_count))
        row_size = self._table_structure.get_row_size()
        details.extend(self._to_long_little_endian(row_size))
        details.extend([0] * 24)
        for row in self._data:
            details.extend(
                self._table_structure.get_row_data_for_details(row, start_column_index=self._start_column_index))
        return details

    def _validate_data(self, structure, data, start_column_index):
        struct_error_msg = "Data should be a list of lists or values which represents a list of rows with values to be written."
        if type(data) is not list:
            raise ValueError(struct_error_msg)
        if any(type(r) is not list for r in data):
            raise ValueError(struct_error_msg)
        if len(data) == 0:
            raise ValueError("Data is empty!")
        for row in data:
            structure.validate_row_values(row, start_column_index=start_column_index)

    def parse_reply(self, buffer: bytearray):
        reply = super().parse_reply(buffer)
        if len(reply) != 0:
            raise WriteDatatableError(self._table_structure.name, self._data, reply)


class WriteDatatableError(Exception):
    def __init__(self, table_name, data, reply):
        msg = "An error occured while writing to datatable '%s'.\nData: %s\nReply: %s"
        super().__init__(msg % (table_name, data, reply))
