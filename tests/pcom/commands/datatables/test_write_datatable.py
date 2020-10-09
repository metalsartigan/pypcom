from .base_test import BaseTest
from mock import MagicMock, patch
from pcom.commands import datatables


class TestWriteDatatable(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self._data = [
            ["abcde", [40000], [True] * 9, [False], [True], [200, 300], [11]],
            ["fgh  ", [50000], [True] * 9, [True], [False], [100, 50], [12]]
        ]
        self._command = datatables.WriteDatatable(structure=self._structure, start_row_index=3, start_column_index=1,
                                                  data=self._data)

    def test_get_bytes_specific(self):
        expected = bytearray(b'/_OPLC\x00\xfe\x01\x00\x00\x00D\x00f\x00\x00\x00\x00\x00D\x00W\xfc\x12\x00\x02\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00abcde@\x9c\x00\x00\xff\x01\x00\x01\xc8\x00,\x01\x0bfgh  P\xc3\x00\x00\xff\x01\x01\x00d\x002\x00\x0c\xe2\xf6\\')

        actual = self._command.get_bytes()

        self.assertEqual(expected, actual)

    def test_parse_reply(self):
        structure = datatables.DatatableStructure("Test", offset=0, rows=500, columns=[datatables.Bool()])
        command = datatables.WriteDatatable(structure=structure)
        raw_reply = bytearray(b'/_OPLC\xfe\x00\x01\x00\x00\x00\xc4d\xe8N\x00\x00\x00\x00\x00\x00\xe7\xfa\x00\x00\\')

        actual = command.parse_reply(raw_reply)

        self.assertIsNone(actual)

    def test_parse_reply(self):
        from pcom.commands.datatables.write_datatable import DatatableCommand
        with patch.object(DatatableCommand, 'parse_reply', return_value=bytearray(b'\x01')):
            with self.assertRaises(datatables.WriteDatatableError):
                self._command.parse_reply(MagicMock())

    def test_invalid_data(self):
        data = [
            [[12], "x", [40000], [True] * 9, [False], [True], [200, 300], [12]]
        ]
        with self.assertRaises(ValueError, msg="String is too short"):
            datatables.WriteDatatable(structure=self._structure, data=data)

    def test_invalid_data_structure(self):
        data = [[12], "abcde", [40000], [True] * 9, [False], [True], [200, 300], [12]]
        with self.assertRaises(ValueError, msg="Row not in list of rows"):
            datatables.WriteDatatable(structure=self._structure, data=data)
        with self.assertRaises(ValueError, msg="Empty row list"):
            datatables.WriteDatatable(structure=self._structure, data=[])
        with self.assertRaises(ValueError, msg="Data is not a list"):
            datatables.WriteDatatable(structure=self._structure, data="HELLO!")
