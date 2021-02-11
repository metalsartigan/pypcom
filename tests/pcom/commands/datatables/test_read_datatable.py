from .base_test import BaseTest
from pcom.commands import datatables


class TestReadDatatable(BaseTest):
    def test_get_bytes_specific(self):
        command = datatables.ReadDatatable(structure=self._structure, start_row_index=3, row_count=10,
                                           start_column_index=1, column_count=2)
        expected = bytearray(
            b'/_OPLC\x00\xfe\x01\x00\x00\x00\x04\x00f\x00\x00\x00\x00\x00 \x00\xbb\xfc\t\x00\n\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xda\xff\\')

        actual = command.get_bytes()

        self.assertEqual(expected, actual)

    def test_get_bytes_default_column_and_row_count(self):
        command = datatables.ReadDatatable(structure=self._structure, start_row_index=3,
                                           start_column_index=1)
        expected = bytearray(
            b'/_OPLC\x00\xfe\x01\x00\x00\x00\x04\x00f\x00\x00\x00\x00\x00 \x00\xbb\xfc\x12\x00\x13\x00\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc8\xff\\')

        actual = command.get_bytes()

        self.assertEqual(expected, actual)

    def test_parse_reply(self):
        structure = datatables.DatatableStructure("Test", offset=0, rows=500, columns=[
            datatables.ULong(),
            datatables.ULong(),
            datatables.ULong(),
            datatables.Bool(),
            datatables.Long(),
            datatables.Long(),
            datatables.Long(),
            datatables.Int(),
            datatables.Int(),
            datatables.Int(),
            datatables.Byte(),
            datatables.Int(),
            datatables.Int(),
            datatables.Bool(),
            datatables.Bool(),
        ])
        command = datatables.ReadDatatable(structure=structure, start_row_index=15, row_count=2)
        raw_reply = bytearray(
            b'/_OPLC\xfe\x00\x01\x00\x00\x00\x84d\x00\x00\x00\x00\x00\x00L\x00\x11\xfc\t\xca\x9a;\xcc\xa35w\xaa\xfb.\xb5\x01\x99\xbc\x00\x00\x02\x04\xf2 @h\x82A\xe4\x07b\x02\xe2\x04\x19\x16\xd0 \x80\x00\x00\t\xca\x9a;3\xa35ww!\x02\xb3\x00k;\x00\x00\x02\x04\xf2 @h\x82A\xe4\x07b\x02\xda\x04(\x16\xd0 \x80\x00\x00\x8d\xe6\\')

        actual = command.parse_reply(raw_reply)

        expected = [
            [[1000000009], [2000004044], [3039755178], [True], [48281], [552731650], [1099065408], [2020], [610],
             [1250], [25], [-12266], [-32736], [False], [False]],
            [[1000000009], [2000003891], [3003261303], [False], [15211], [552731650], [1099065408], [2020], [610],
             [1242], [40], [-12266], [-32736], [False], [False]],
        ]

        self.assertListEqual(expected, actual)
