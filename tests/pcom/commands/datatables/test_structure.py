from .base_test import BaseTest

from pcom.commands import datatables


class TestStructure(BaseTest):
    def test_data_types_invalid_size(self):
        with self.assertRaises(ValueError):
            datatables.String(0)
        with self.assertRaises(ValueError):
            datatables.String(-1)

    def test_data_types_size(self):
        self.assertEqual(1, datatables.Bool().size)
        self.assertEqual(1, datatables.Bool(8).size)
        self.assertEqual(2, datatables.Bool(9).size)
        self.assertEqual(2, datatables.Bool(16).size)
        self.assertEqual(3, datatables.Bool(17).size)
        self.assertEqual(18, datatables.String(18).size)
        self.assertEqual(1, datatables.String(1).size)
        self.assertEqual(1, datatables.Byte().size)
        self.assertEqual(2, datatables.Int().size)
        self.assertEqual(2, datatables.UInt().size)
        self.assertEqual(4, datatables.Long().size)
        self.assertEqual(4, datatables.ULong().size)

    def test_properties(self):
        self.assertEqual("Some table", self._structure.name)
        self.assertEqual(44, self._structure.offset)
        self.assertEqual(22, self._structure.rows)
        self.assertListEqual(self._columns, self._structure.columns)

    def test_get_cell_offset(self):
        self.assertEqual(44 + (0 * 15) + 0, self._structure.get_cell_offset(0, 0), msg="0, 0")
        self.assertEqual(44 + (0 * 15) + 6, self._structure.get_cell_offset(0, 2), msg="0, 2")
        self.assertEqual(44 + (0 * 15) + 10, self._structure.get_cell_offset(0, 3), msg="0, 3")
        self.assertEqual(44 + (0 * 15) + 12, self._structure.get_cell_offset(0, 4), msg="0, 4")
        with self.assertRaises(ValueError, msg="Trying to get offset at end of row"):
            self._structure.get_cell_offset(0, 15)

        self.assertEqual(44 + (2 * 15) + 0, self._structure.get_cell_offset(2, 0), msg="2, 0")
        self.assertEqual(44 + (2 * 15) + 6, self._structure.get_cell_offset(2, 2), msg="2, 2")
        self.assertEqual(44 + (2 * 15) + 10, self._structure.get_cell_offset(2, 3), msg="2, 3")
        self.assertEqual(44 + (2 * 15) + 12, self._structure.get_cell_offset(2, 4), msg="2, 4")
        self.assertEqual(44 + (21 * 15) + 10, self._structure.get_cell_offset(21, 3), msg="21, 3")
        with self.assertRaises(ValueError, msg="Trying to get offset for row after end of datatable"):
            self._structure.get_cell_offset(22, 3)

    def test_get_row_size(self):
        self.assertEqual(6, self._structure.get_row_size(0, 2), msg="(0, 2)")
        self.assertEqual(9, self._structure.get_row_size(1, 2), msg="(1, 2)")
        self.assertEqual(14, self._structure.get_row_size(1), msg="(1)")
        self.assertEqual(12, self._structure.get_row_size(0, 4), msg="(0, 4)")
        self.assertEqual(15, self._structure.get_row_size(), msg="()")
        self.assertEqual(1, self._structure.get_row_size(6), msg="(7)")
        with self.assertRaises(ValueError):
            self._structure.get_row_size(-1, 1)
        with self.assertRaises(ValueError):
            self._structure.get_row_size(-1, 7)
        with self.assertRaises(ValueError, msg="Cannot get size for more columns"):
            self._structure.get_row_size(0, 8)
        with self.assertRaises(ValueError, msg="Cannot get size starting after last column"):
            self._structure.get_row_size(7)
        with self.assertRaises(ValueError):
            self._structure.get_row_size(0, -1)

    def test_bool_parse_value_single(self):
        col = datatables.Bool()
        self.assertListEqual([False], col.parse_value([0x00]))
        self.assertListEqual([True], col.parse_value([0x01]))
        self.assertListEqual([True], col.parse_value([0xFF]))

    def test_bool_parse_value_multiple_bools_single_byte(self):
        col = datatables.Bool(8)
        self.assertListEqual([False, False, False, False, False, False, False, False], col.parse_value([0x00]))
        self.assertListEqual([True, False, False, False, False, False, False, False], col.parse_value([0x01]))
        self.assertListEqual([False, False, False, False, False, False, False, True], col.parse_value([0x80]))
        self.assertListEqual([True, True, True, True, True, True, True, True], col.parse_value([0xFF]))

    def test_bool_parse_value_multiple_boole_multiple_bytes(self):
        col = datatables.Bool(9)
        self.assertListEqual([False, False, False, False, False, False, False, False, False], col.parse_value([0x00, 0x00]))
        self.assertListEqual([True, False, False, False, False, False, False, False, False], col.parse_value([0x01, 0x00]))
        self.assertListEqual([False, False, False, False, False, False, False, False, True], col.parse_value([0x00, 0x01]))
        self.assertListEqual([True, True, True, True, True, True, True, True, True], col.parse_value([0xFF, 0x01]))
        self.assertListEqual([True, True, True, True, True, True, True, True, True], col.parse_value([0xFF, 0xFF]))

    def test_int_parse_value(self):
        col = datatables.Int()
        self.assertEqual(4531, col.parse_value([0xb3, 0x11]))
        self.assertEqual(0, col.parse_value([0x00, 0x00]))
        self.assertEqual(-1, col.parse_value([0xFF, 0xFF]))
        self.assertEqual(-32768, col.parse_value([0x00, 0x80]))
        self.assertEqual(32767, col.parse_value([0xFF, 0x7F]))

    def test_long_parse_value(self):
        col = datatables.Long()
        self.assertEqual(3464531, col.parse_value([0x53, 0xDD, 0x34, 0x00]))
        self.assertEqual(0, col.parse_value([0x00, 0x00, 0x00, 0x00]))
        self.assertEqual(-1, col.parse_value([0xFF, 0xFF, 0xFF, 0xFF]))
        self.assertEqual(-2147483648, col.parse_value([0x00, 0x00, 0x00, 0x80]))
        self.assertEqual(2147483647, col.parse_value([0xFF, 0xFF, 0xFF, 0x7F]))

    def test_uint_parse_value(self):
        col = datatables.UInt()
        self.assertEqual(4531, col.parse_value([0xb3, 0x11]))
        self.assertEqual(0, col.parse_value([0x00, 0x00]))
        self.assertEqual(65535, col.parse_value([0xFF, 0xFF]))

    def test_ulong_parse_value(self):
        col = datatables.ULong()
        self.assertEqual(3464531, col.parse_value([0x53, 0xDD, 0x34, 0x00]))
        self.assertEqual(0, col.parse_value([0x00, 0x00, 0x00, 0x00]))
        self.assertEqual(0xFFFFFFFF, col.parse_value([0xFF, 0xFF, 0xFF, 0xFF]))

    def test_byte_parse_value(self):
        col = datatables.Byte()
        self.assertEqual(0, col.parse_value([0x0]))
        self.assertEqual(13, col.parse_value([0x0D]))
        self.assertEqual(255, col.parse_value([0xFF]))

    def test_string_parse_value(self):
        col = datatables.String(5)
        self.assertEqual("BONJOUR", col.parse_value([0x42, 0x4f, 0x4e, 0x4a, 0x4f, 0x55, 0x52]))

    def test_float_parse_value(self):
        col = datatables.Float()
        self.assertEqual(0, col.parse_value([0x0, 0x0, 0x0, 0x0]))
        self.assertAlmostEqual(12345.67, col.parse_value([0x40, 0x46, 0xae, 0xe6]), places=2)

    def test_timer_parse_value(self):
        col = datatables.Timer()
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.assertListEqual(expected, col.parse_value(expected))
        self.skipTest("Lacking documentation on this. It's not supported yet.")
        # https://forum.unitronics.com/topic/7631-how-to-read-a-timer-column-in-a-datatable/
