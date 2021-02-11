from .base_test import BaseTest

from datetime import timedelta
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
        self.assertEqual(2, datatables.Byte(2).size)
        self.assertEqual(2, datatables.Int().size)
        self.assertEqual(2, datatables.UInt().size)
        self.assertEqual(4, datatables.UInt(2).size)
        self.assertEqual(4, datatables.Long().size)
        self.assertEqual(4, datatables.ULong().size)
        self.assertEqual(8, datatables.ULong(2).size)
        self.assertEqual(4, datatables.Float().size)
        self.assertEqual(8, datatables.Float(2).size)
        self.assertEqual(12, datatables.Timer().size)
        self.assertEqual(24, datatables.Timer(2).size)

    def test_properties(self):
        self.assertEqual("Some table", self._structure.name)
        self.assertEqual(44, self._structure.offset)
        self.assertEqual(22, self._structure.rows)
        self.assertListEqual(self._columns, self._structure.columns)

    def test_get_cell_offset(self):
        self.assertEqual(44 + (0 * 19) + 0, self._structure.get_cell_offset(0, 0), msg="0, 0")
        self.assertEqual(44 + (0 * 19) + 6, self._structure.get_cell_offset(0, 2), msg="0, 2")
        self.assertEqual(44 + (0 * 19) + 10, self._structure.get_cell_offset(0, 3), msg="0, 3")
        self.assertEqual(44 + (0 * 19) + 12, self._structure.get_cell_offset(0, 4), msg="0, 4")
        with self.assertRaises(ValueError, msg="Trying to get offset at end of row"):
            self._structure.get_cell_offset(0, 15)

        self.assertEqual(44 + (2 * 19) + 0, self._structure.get_cell_offset(2, 0), msg="2, 0")
        self.assertEqual(44 + (2 * 19) + 6, self._structure.get_cell_offset(2, 2), msg="2, 2")
        self.assertEqual(44 + (2 * 19) + 10, self._structure.get_cell_offset(2, 3), msg="2, 3")
        self.assertEqual(44 + (2 * 19) + 12, self._structure.get_cell_offset(2, 4), msg="2, 4")
        self.assertEqual(44 + (21 * 19) + 10, self._structure.get_cell_offset(21, 3), msg="21, 3")
        with self.assertRaises(ValueError, msg="Trying to get offset for row after end of datatable"):
            self._structure.get_cell_offset(22, 3)

    def test_get_row_size(self):
        self.assertEqual(6, self._structure.get_row_size(0, 2), msg="(0, 2)")
        self.assertEqual(9, self._structure.get_row_size(1, 2), msg="(1, 2)")
        self.assertEqual(18, self._structure.get_row_size(1), msg="(1)")
        self.assertEqual(12, self._structure.get_row_size(0, 4), msg="(0, 4)")
        self.assertEqual(19, self._structure.get_row_size(), msg="()")
        self.assertEqual(1, self._structure.get_row_size(7), msg="(7)")
        with self.assertRaises(ValueError):
            self._structure.get_row_size(-1, 1)
        with self.assertRaises(ValueError):
            self._structure.get_row_size(-1, 7)
        with self.assertRaises(ValueError, msg="Cannot get size for more columns"):
            self._structure.get_row_size(0, 9)
        with self.assertRaises(ValueError, msg="Cannot get size starting after last column"):
            self._structure.get_row_size(8)
        with self.assertRaises(ValueError):
            self._structure.get_row_size(0, -1)

    def test_get_row_count(self):
        self.assertEqual(2, self._structure.get_row_count(0, 2), msg="(0, 2)")
        self.assertEqual(2, self._structure.get_row_count(1, 2), msg="(1, 2)")
        self.assertEqual(22, self._structure.get_row_count(0, 22), msg="(0, 22)")
        self.assertEqual(22, self._structure.get_row_count(0, 0), msg="(0, 0)")
        self.assertEqual(20, self._structure.get_row_count(2, 0), msg="(2, 0)")
        self.assertEqual(10, self._structure.get_row_count(2, 10), msg="(2, 10)")
        with self.assertRaises(ValueError):
            self._structure.get_row_count(-1, 0)
        with self.assertRaises(ValueError, msg="Cannot get count for more rows"):
            self._structure.get_row_count(0, 23)
        with self.assertRaises(ValueError, msg="Cannot get count starting after last row"):
            self._structure.get_row_count(22, 0)
        with self.assertRaises(ValueError):
            self._structure.get_row_count(0, -1)

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
        self.assertListEqual([4531], col.parse_value([0xb3, 0x11]))
        self.assertListEqual([0], col.parse_value([0x00, 0x00]))
        self.assertListEqual([-1], col.parse_value([0xFF, 0xFF]))
        col = datatables.Int(2)
        self.assertListEqual([-32768, 32767], col.parse_value([0x00, 0x80, 0xFF, 0x7F]))

    def test_long_parse_value(self):
        col = datatables.Long()
        self.assertListEqual([3464531], col.parse_value([0x53, 0xDD, 0x34, 0x00]))
        self.assertListEqual([0], col.parse_value([0x00, 0x00, 0x00, 0x00]))
        self.assertListEqual([-1], col.parse_value([0xFF, 0xFF, 0xFF, 0xFF]))
        col = datatables.Long(2)
        self.assertListEqual([-2147483648, 2147483647], col.parse_value([0x00, 0x00, 0x00, 0x80, 0xFF, 0xFF, 0xFF, 0x7F]))

    def test_uint_parse_value(self):
        col = datatables.UInt()
        self.assertListEqual([4531], col.parse_value([0xb3, 0x11]))
        col = datatables.UInt(2)
        self.assertListEqual([0, 65535], col.parse_value([0x00, 0x00, 0xFF, 0xFF]))

    def test_ulong_parse_value(self):
        col = datatables.ULong()
        self.assertListEqual([3464531], col.parse_value([0x53, 0xDD, 0x34, 0x00]))
        col = datatables.ULong(2)
        self.assertListEqual([0, 0xFFFFFFFF], col.parse_value([0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF]))

    def test_byte_parse_value(self):
        col = datatables.Byte()
        self.assertListEqual([0], col.parse_value([0x0]))
        col = datatables.Byte(2)
        self.assertListEqual([13, 255], col.parse_value([0x0D, 0xFF]))

    def test_string_parse_value(self):
        col = datatables.String(5)
        self.assertEqual("BONJOUR", col.parse_value([0x42, 0x4f, 0x4e, 0x4a, 0x4f, 0x55, 0x52]))

    def test_float_parse_value(self):
        col = datatables.Float()
        self.assertListEqual([0], col.parse_value([0x0, 0x0, 0x0, 0x0]))
        col = datatables.Float(2)
        actual = col.parse_value([0x40, 0x46, 0xae, 0xe6, 0x95, 0x47, 0x9b, 0x7f])
        self.assertEqual(2, len(actual))
        self.assertAlmostEqual(12345.67, actual[0], places=2)
        self.assertAlmostEqual(76543.21, actual[1], places=2)

    def test_timer_parse_value(self):
        col = datatables.Timer(3)
        buffer = [
            0, 0, 255, 80, 37, 2, 0, 0, 0, 0, 0, 0,  # max value
            0, 0, 64, 49, 247, 0, 0, 0, 0, 0, 0, 0,  # middle value
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0       # 0 value
        ]
        expected = [
            timedelta(hours=99, minutes=59, seconds=59, milliseconds=990),
            timedelta(hours=45),
            timedelta()
        ]

        self.assertListEqual(expected, col.parse_value(buffer))

    def test_bool_get_data_for_details_single(self):
        col = datatables.Bool()
        self.assertEqual([0x00], col.get_data_for_details([False]))
        self.assertEqual([0x01], col.get_data_for_details([True]))

    def test_bool_get_data_for_details_multiple_bools_single_byte(self):
        col = datatables.Bool(8)
        self.assertEqual([0x00], col.get_data_for_details([False, False, False, False, False, False, False, False]))
        self.assertEqual([0x01], col.get_data_for_details([True, False, False, False, False, False, False, False]))
        self.assertEqual([0x80], col.get_data_for_details([False, False, False, False, False, False, False, True]))
        self.assertEqual([0xff], col.get_data_for_details([True, True, True, True, True, True, True, True]))

    def test_bool_get_data_for_details_multiple_boole_multiple_bytes(self):
        col = datatables.Bool(9)
        self.assertEqual([0x00, 0x00], col.get_data_for_details([False, False, False, False, False, False, False, False, False]))
        self.assertEqual([0x01, 0x00], col.get_data_for_details([True, False, False, False, False, False, False, False, False]))
        self.assertEqual([0x00, 0x01], col.get_data_for_details([False, False, False, False, False, False, False, False, True]))
        self.assertEqual([0xff, 0x01], col.get_data_for_details([True, True, True, True, True, True, True, True, True]))

    def test_int_get_data_for_details(self):
        col = datatables.Int()
        self.assertEqual([0xff, 0xff], col.get_data_for_details([-1]))
        col = datatables.Int(2)
        self.assertEqual([0xb3, 0x11, 0xb2, 0x11], col.get_data_for_details([4531, 4530]))
        self.assertEqual([0x00, 0x00, 0x00, 0x00], col.get_data_for_details([0, 0]))
        self.assertEqual([0x00, 0x80, 0xff, 0x7f], col.get_data_for_details([-32768, 32767]))

    def test_long_get_data_for_details(self):
        col = datatables.Long(2)
        self.assertEqual([0x53, 0xdd, 0x34, 0x00, 0x00, 0x00, 0x00, 0x00], col.get_data_for_details([3464531, 0]))
        col = datatables.Long()
        self.assertEqual([0xff, 0xff, 0xff, 0xff], col.get_data_for_details([-1]))
        self.assertEqual([0x00, 0x00, 0x00, 0x80], col.get_data_for_details([-2147483648]))
        self.assertEqual([0xff, 0xff, 0xff, 0x7f], col.get_data_for_details([2147483647]))

    def test_uint_get_data_for_details(self):
        col = datatables.UInt(2)
        self.assertEqual([0xb3, 0x11, 0x00, 0x00], col.get_data_for_details([4531, 0]))
        col = datatables.UInt()
        self.assertEqual([0xff, 0xff], col.get_data_for_details([65535]))

    def test_ulong_get_data_for_details(self):
        col = datatables.ULong(2)
        self.assertEqual([0x53, 0xdd, 0x34, 0x00, 0x00, 0x00, 0x00, 0x00], col.get_data_for_details([3464531, 0]))
        col = datatables.ULong()
        self.assertEqual([0xff, 0xff, 0xff, 0xff], col.get_data_for_details([0xFFFFFFFF]))

    def test_byte_get_data_for_details(self):
        col = datatables.Byte(2)
        self.assertEqual([0x00, 0x0d], col.get_data_for_details([0, 13]))
        col = datatables.Byte()
        self.assertEqual([0xff], col.get_data_for_details([255]))

    def test_string_get_data_for_details(self):
        col = datatables.String(5)
        self.assertEqual([0x42, 0x4f, 0x4e, 0x4a, 0x4f, 0x55, 0x52], col.get_data_for_details("BONJOUR"))

    def test_float_get_data_for_details(self):
        col = datatables.Float(2)
        self.assertEqual([0x00, 0x00, 0x00, 0x00, 0x40, 0x46, 0xae, 0xe6], col.get_data_for_details([0, 12345.67]))
        col = datatables.Float()
        self.assertEqual([0x40, 0x46, 0xae, 0xe6], col.get_data_for_details([12345.67]))

    def test_timer_get_data_for_details(self):
        col = datatables.Timer(2)
        expected = [
            0, 0, 255, 80, 37, 2, 0, 0, 0, 0, 0, 0,  # max value
            0, 0, 64, 49, 247, 0, 0, 0, 0, 0, 0, 0,  # middle value
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # 0 value
        ]
        details = [
            timedelta(hours=99, minutes=59, seconds=59, milliseconds=990),
            timedelta(hours=45),
            timedelta()
        ]

        self.assertListEqual(expected, col.get_data_for_details(details))

    def test_validate_values_bool(self):
        datatables.Bool().validate_values([True])
        datatables.Bool(2).validate_values([True, False])

        with self.assertRaises(ValueError, msg="Too many values"):
            datatables.Bool().validate_values([True, False])
        with self.assertRaises(ValueError, msg="Not enough values values"):
            datatables.Bool(2).validate_values([False])
        with self.assertRaises(ValueError, msg="Type mismatch"):
            datatables.Bool(2).validate_values([1, False])

    def test_validate_values_string(self):
        datatables.String(1).validate_values("a")

        with self.assertRaises(ValueError, msg="Too many values"):
            datatables.String(2).validate_values("abc")
        with self.assertRaises(ValueError, msg="Not enough values values"):
            datatables.String(2).validate_values("a")
        with self.assertRaises(ValueError, msg="Type mismatch"):
            datatables.String(2).validate_values([1, 2])

    def test_validate_values_byte(self):
        datatables.Byte().validate_values([1])
        datatables.Byte(2).validate_values([0, 255])

        with self.assertRaises(ValueError, msg="Too many values"):
            datatables.Byte().validate_values([1, 2])
        with self.assertRaises(ValueError, msg="Not enough values values"):
            datatables.Byte(2).validate_values([1])
        with self.assertRaises(ValueError, msg="Low value"):
            datatables.Byte(2).validate_values([2, -2])
        with self.assertRaises(ValueError, msg="High value"):
            datatables.Byte(2).validate_values([256, 1])
        with self.assertRaises(ValueError, msg="Type mismatch"):
            datatables.Byte(2).validate_values([1, False])

    def test_validate_values_uint(self):
        datatables.UInt().validate_values([1])
        datatables.UInt(2).validate_values([0, 65535])

        with self.assertRaises(ValueError, msg="Too many values"):
            datatables.UInt().validate_values([1, 2])
        with self.assertRaises(ValueError, msg="Not enough values values"):
            datatables.UInt(2).validate_values([1])
        with self.assertRaises(ValueError, msg="Low value"):
            datatables.UInt(2).validate_values([2, -2])
        with self.assertRaises(ValueError, msg="High value"):
            datatables.UInt(2).validate_values([65536, 1])
        with self.assertRaises(ValueError, msg="Type mismatch"):
            datatables.UInt(2).validate_values([1, False])

    def test_validate_values_int(self):
        datatables.Int().validate_values([1])
        datatables.Int(2).validate_values([-32768, 32767])

        with self.assertRaises(ValueError, msg="Too many values"):
            datatables.Int().validate_values([1, 2])
        with self.assertRaises(ValueError, msg="Not enough values values"):
            datatables.Int(2).validate_values([1])
        with self.assertRaises(ValueError, msg="Low value"):
            datatables.Int(2).validate_values([2, -32769])
        with self.assertRaises(ValueError, msg="High value"):
            datatables.Int(2).validate_values([32768, 1])
        with self.assertRaises(ValueError, msg="Type mismatch"):
            datatables.Int(2).validate_values([1, False])

    def test_validate_values_ulong(self):
        datatables.ULong().validate_values([1])
        datatables.ULong(2).validate_values([0, 4294967295])

        with self.assertRaises(ValueError, msg="Too many values"):
            datatables.ULong().validate_values([1, 2])
        with self.assertRaises(ValueError, msg="Not enough values values"):
            datatables.ULong(2).validate_values([1])
        with self.assertRaises(ValueError, msg="Low value"):
            datatables.ULong(2).validate_values([2, -2])
        with self.assertRaises(ValueError, msg="High value"):
            datatables.ULong(2).validate_values([4294967296, 1])
        with self.assertRaises(ValueError, msg="Type mismatch"):
            datatables.ULong(2).validate_values([1, False])

    def test_validate_values_long(self):
        datatables.Long().validate_values([1])
        datatables.Long(2).validate_values([-2147483648, 2147483647])

        with self.assertRaises(ValueError, msg="Too many values"):
            datatables.Long().validate_values([1, 2])
        with self.assertRaises(ValueError, msg="Not enough values values"):
            datatables.Long(2).validate_values([1])
        with self.assertRaises(ValueError, msg="Low value"):
            datatables.Long(2).validate_values([2, -2147483649])
        with self.assertRaises(ValueError, msg="High value"):
            datatables.Long(2).validate_values([2147483648, 1])
        with self.assertRaises(ValueError, msg="Type mismatch"):
            datatables.Long(2).validate_values([1, False])

    def test_validate_values_float(self):
        datatables.Float().validate_values([1])
        datatables.Float(2).validate_values([-1.18e-38, 2147483647])

        with self.assertRaises(ValueError, msg="Too many values"):
            datatables.Float().validate_values([1, 2])
        with self.assertRaises(ValueError, msg="Not enough values values"):
            datatables.Float(2).validate_values([1])
        with self.assertRaises(ValueError, msg="Low value"):
            datatables.Float(2).validate_values([2, -3.5e+38])
        with self.assertRaises(ValueError, msg="High value"):
            datatables.Float(2).validate_values([3.5e+38, 1])
        with self.assertRaises(ValueError, msg="Type mismatch"):
            datatables.Float(2).validate_values([1, False])

    def test_validate_values_timer(self):
        datatables.Timer().validate_values([timedelta()])
        datatables.Timer(2).validate_values([timedelta()] * 2)
        datatables.Timer().validate_values([timedelta(hours=99, minutes=59, seconds=59, milliseconds=990)])

        with self.assertRaises(ValueError, msg="Too many values"):
            datatables.Timer().validate_values([timedelta()] * 2)
        with self.assertRaises(ValueError, msg="Not enough values"):
            datatables.Timer(2).validate_values([timedelta()])
        with self.assertRaises(ValueError, msg="Type mismatch"):
            datatables.Timer(2).validate_values([timedelta(), False])
        with self.assertRaises(ValueError, msg="Value too high"):
            datatables.Timer().validate_values([timedelta(hours=99, minutes=59, seconds=59, milliseconds=991)])

    def test_datatable_structure_validate_row_values(self):
        row = [[12], "abcde", [12345678], [True] * 9, [False], [True], [1024, 2048], [1]]
        self._structure.validate_row_values(row, start_column_index=0)

    def test_datatable_structure_validate_row_values_no_value(self):
        with self.assertRaises(ValueError):
            self._structure.validate_row_values([], start_column_index=0)

    def test_datatable_structure_validate_row_values_missing_value(self):
        row = [[12], "abcde", [12345678], [True] * 9, [True], [1024, 2048], [1]]
        with self.assertRaises(ValueError):
            self._structure.validate_row_values(row, start_column_index=0)

    def test_datatable_structure_validate_row_values_less_values(self):
        row = ["abcde", [12345678]]
        self._structure.validate_row_values(row, start_column_index=1)

    def test_datatable_structure_validate_row_values_extra_value(self):
        row = [[12], "abcde", [12345678], [42, 42, 42], [True] * 9, [False], [True], [1024, 2048], [1]]
        with self.assertRaises(ValueError):
            self._structure.validate_row_values(row, start_column_index=0)

    def test_datatable_structure_validate_row_values_invalid_value(self):
        row = [[12], "x", [12345678], [True] * 9, [False], [True], [1024, 2048], [1]]
        with self.assertRaises(ValueError):
            self._structure.validate_row_values(row, start_column_index=0)

    def test_datatable_structure_validate_row_values_invalid_start_column_index(self):
        row = [[12], "abcde", [12345678], [True] * 9, [False], [True], [1024, 2048], [1]]
        with self.assertRaises(ValueError):
            self._structure.validate_row_values(row, start_column_index=-1)
        with self.assertRaises(ValueError):
            self._structure.validate_row_values(row, start_column_index=len(row))
        with self.assertRaises(ValueError):
            self._structure.validate_row_values(row, start_column_index=1)

    def test_datatable_structure_get_row_data_for_details_full(self):
        row = [[12], "abcde", [12345678], [True] * 9, [False], [True], [1024, 2048], [1]]
        expected = [12, 97, 98, 99, 100, 101, 78, 97, 188, 0, 0xff, 0x01, 0x00, 0x01, 0x00, 0x04, 0x00, 0x08, 0x01]

        actual = self._structure.get_row_data_for_details(row, start_column_index=0)

        self.assertListEqual(expected, actual)

    def test_datatable_structure_get_row_data_for_details_start_index(self):
        row = [[12345678], [True] * 9, [False], [True], [1024, 2048], [1]]
        expected = [78, 97, 188, 0, 0xff, 0x01, 0x00, 0x01, 0x00, 0x04, 0x00, 0x08, 0x01]

        actual = self._structure.get_row_data_for_details(row, start_column_index=2)

        self.assertListEqual(expected, actual)

    def test_datatable_structure_get_row_data_for_details_start_index_partial(self):
        row = [[12345678], [True] * 9, [False], [True]]
        expected = [78, 97, 188, 0, 0xff, 0x01, 0x00, 0x01]

        actual = self._structure.get_row_data_for_details(row, start_column_index=2)

        self.assertListEqual(expected, actual)

    def test_datatable_structure_get_row_data_for_details_invalid_start_index(self):
        row = [[12], "abcde", [12345678], [True] * 9, [False], [True], [1024, 2048], [1]]
        with self.assertRaises(ValueError):
            self._structure.get_row_data_for_details(row, start_column_index=-1)
        with self.assertRaises(ValueError):
            self._structure.get_row_data_for_details(row, start_column_index=len(row))

    def test_parse_reply_partial_row(self):
        columns = [
            datatables.Byte(),
            datatables.String(5),
            datatables.Timer(),
            datatables.Bool(9),
        ]
        structure = datatables.DatatableStructure("Some table", offset=44, rows=22, columns=columns)
        reply = bytearray(b'\x00\x00\xffP%\x02\x00\x00\x00\x00\x00\x00')
        expected = [[[timedelta(hours=99, minutes=59, seconds=59, milliseconds=990)]]]

        actual = structure.parse_reply(reply, start_column_index=2, column_count=1)

        self.assertListEqual(expected, actual)
