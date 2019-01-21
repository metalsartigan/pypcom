from unittest import TestCase

from pcom.commands import CommandReadOperands
from pcom.commands import operand_request


class TestCommandReadOperands(TestCase):
    def setUp(self):
        super().setUp()
        self._command = CommandReadOperands(plc_id=0)

    def test_request_codes(self):
        self.assertEqual(0x01, operand_request.MB(addresses=[]).code)
        self.assertEqual(0x02, operand_request.SB(addresses=[]).code)
        self.assertEqual(0x03, operand_request.MI(addresses=[]).code)
        self.assertEqual(0x04, operand_request.SI(addresses=[]).code)
        self.assertEqual(0x05, operand_request.ML(addresses=[]).code)
        self.assertEqual(0x06, operand_request.SL(addresses=[]).code)
        self.assertEqual(0x07, operand_request.MF(addresses=[]).code)
        self.assertEqual(0x08, operand_request.SF(addresses=[]).code)
        self.assertEqual(0x09, operand_request.Input(addresses=[]).code)
        self.assertEqual(0x0a, operand_request.Output(addresses=[]).code)
        self.assertEqual(0x0b, operand_request.TimerRunBit(addresses=[]).code)
        self.assertEqual(0x0c, operand_request.CounterRunBit(addresses=[]).code)
        self.assertEqual(0x10, operand_request.DW(addresses=[]).code)
        self.assertEqual(0x11, operand_request.SDW(addresses=[]).code)
        self.assertEqual(0x12, operand_request.CounterCurrent(addresses=[]).code)
        self.assertEqual(0x13, operand_request.CounterPreset(addresses=[]).code)
        self.assertEqual(0x14, operand_request.TimerCurrent(addresses=[]).code)
        self.assertEqual(0x15, operand_request.TimerPreset(addresses=[]).code)

    def test_read_MB_1(self):
        self._init_example_1()

        expected = bytearray([0x2F, 0x5F, 0x4F, 0x50, 0x4C, 0x43, 0x00, 0xFE, 0x01, 0x00, 0x00, 0x00, 0x4D, 0x00,
                              0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x06, 0x00, 0xF1, 0xFC,
                              0x01, 0x00, 0x01, 0xFF, 0x01, 0x00,
                              0xFE, 0xFE, 0x5C])
        self.assert_command(expected)

    def test_read_MB_MF_MI_non_vector(self):
        self._init_example_2()

        expected = bytearray(
            [0x2F, 0x5F, 0x4F, 0x50, 0x4C, 0x43, 0x00, 0xFE, 0x01, 0x00, 0x00, 0x00, 0x4D, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x03, 0x00, 0x22, 0x00, 0xD3, 0xFC,
             0x07, 0x00, 0x01, 0xFF, 0x01, 0x00, 0x02, 0x00, 0x03, 0x00, 0x04, 0x00, 0x05, 0x00, 0x06, 0x00, 0x07, 0x00,
             0x03, 0x00, 0x03, 0xFF, 0x01, 0x00, 0x02, 0x00, 0x03, 0x00, 0x01, 0x00, 0x07, 0xFF, 0x0F, 0x00,
             0xBC, 0xFC, 0x5C])
        self.assert_command(expected)

    def test_read_MB_MI_non_vector(self):
        self._init_example_3()

        expected = bytearray(
            [0x2F, 0x5F, 0x4F, 0x50, 0x4C, 0x43, 0x00, 0xFE, 0x01, 0x00, 0x00, 0x00, 0x4D, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x02, 0x00, 0x1A, 0x00, 0xDC, 0xFC,
             0x06, 0x00, 0x01, 0xFF, 0x01, 0x00, 0x02, 0x00, 0x03, 0x00, 0x04, 0x00, 0x05, 0x00, 0x06, 0x00, 0x03, 0x00,
             0x03, 0xFF, 0x06, 0x00, 0x07, 0x00, 0x08, 0x00,
             0xCB, 0xFD, 0x5C])
        self.assert_command(expected)

    def test_read_MI_vector(self):
        self._init_example_4()
        expected = bytearray(
            [0x2F, 0x5F, 0x4F, 0x50, 0x4C, 0x43, 0x00, 0xFE, 0x01, 0x00, 0x00, 0x00, 0x4D, 0x00, 0x00, 0x00, 0x00, 0x00,
             0x01, 0x00, 0x06, 0x00, 0xF1, 0xFC,
             0x06, 0x00, 0x83, 0xFF, 0x0D, 0x00,
             0x6B, 0xFE, 0x5C])
        self.assert_command(expected)

    def test_read_complex(self):
        self._init_example_complex()

        expected = bytearray(
            [0x2f, 0x5f, 0x4f, 0x50, 0x4c, 0x43, 0x00, 0xfe, 0x01, 0x00, 0x00, 0x00, 0x4d, 0x00, 0x00, 0x00, 0x00, 0x00, 0x16,
             0x00, 0x8c, 0x00, 0x56, 0xfc,
             0x01, 0x00, 0x01, 0xff, 0x4e, 0x00, 0x06, 0x00, 0x81, 0xff, 0x22, 0x00, 0x09, 0x00,
             0x89, 0xff, 0x07, 0x00, 0x01, 0x00, 0x09, 0xff, 0x41, 0x00, 0x02, 0x00, 0x0b, 0xff, 0x22, 0x00, 0x81, 0x00, 0x06,
             0x00, 0x8b, 0xff, 0x2a, 0x00, 0x01, 0x00, 0x0c, 0xff, 0x0f, 0x00, 0x04, 0x00, 0x8c, 0xff, 0x06, 0x00, 0x02, 0x00,
             0x03, 0xff, 0x11, 0x00, 0x13, 0x00, 0x06, 0x00, 0x83, 0xff, 0xfe, 0x03, 0x01, 0x00, 0x12, 0xff, 0x0f, 0x00, 0x01,
             0x00, 0x13, 0xff, 0x0f, 0x00, 0x04, 0x00, 0x92, 0xff, 0x06, 0x00, 0x04, 0x00, 0x93, 0xff, 0x06, 0x00, 0x02, 0x00,
             0x14, 0xff, 0x22, 0x00, 0x81, 0x00, 0x02, 0x00, 0x15, 0xff, 0x22, 0x00, 0x81, 0x00, 0x06, 0x00, 0x94, 0xff, 0x2a,
             0x00, 0x06, 0x00, 0x95, 0xff, 0x2a, 0x00, 0x01, 0x00, 0x05, 0xff, 0x0d, 0x00, 0x03, 0x00, 0x90, 0xff, 0x0c, 0x00,
             0x01, 0x00, 0x07, 0xff, 0x06, 0x00, 0x04, 0x00, 0x87, 0xff, 0x09, 0x00,
             0x9b, 0xde, 0x5c])

        self.assert_command(expected)

    def test_parse_MB_MF_MI_non_vector(self):
        self._init_example_2()
        reply_header = bytearray(
            b'\x2F\x5F\x4F\x50\x4C\x43\xFE\x00\x01\x01\x00\x00\xCD\x00\x00\x00\x00\x00\x03\x00\x0C\x00\x68\xFC')
        reply_details = bytearray(b'\x35\x00\x7B\x00\x7C\x00\x7D\x00\x40\x46\xAE\xE6')
        reply_footer = bytearray(b'\x3D\xFC\x5C')
        reply = reply_header + reply_details + reply_footer

        expected_mb = [True, False, True, False, True, True, False]
        expected_mf = [12345.67]
        expected_mi = [123, 124, 125]

        requests = self._command.parse_reply(reply)
        actual_mb = next(r.values for r in requests if isinstance(r, operand_request.MB))
        actual_mf = next([round(v, 2) for v in r.values] for r in requests if isinstance(r, operand_request.MF))
        actual_mi = next(r.values for r in requests if isinstance(r, operand_request.MI))

        self.assertListEqual(expected_mb, actual_mb)
        self.assertListEqual(expected_mf, actual_mf)
        self.assertListEqual(expected_mi, actual_mi)

    def test_parse_MB_MI_non_vector(self):
        self._init_example_3()

        reply_header = bytearray(
            b'\x2F\x5F\x4F\x50\x4C\x43\xFE\x00\x01\x00\x00\x00\xCD\x00\x00\x00\x00\x00\x02\x00\x08\x00\x6E\xFC')
        reply_details = bytearray(b'\x75\x00\xD2\x04\xD7\x11\x17\x31')
        reply_footer = bytearray(b'\x85\xFD\x5C')
        reply = reply_header + reply_details + reply_footer

        expected_mb = [True, False, True, False, True, True]
        expected_mi = [1234, 4567, 12567]

        requests = self._command.parse_reply(reply)
        actual_mb = next(r.values for r in requests if isinstance(r, operand_request.MB))
        actual_mi = next(r.values for r in requests if isinstance(r, operand_request.MI))

        self.assertListEqual(expected_mb, actual_mb)
        self.assertListEqual(expected_mi, actual_mi)

    def test_parse_MI_vector(self):
        self._init_example_4()
        reply_header = bytearray(
            b'\x2F\x5F\x4F\x50\x4C\x43\xFE\x00\x01\x01\x00\x00\xCD\x00\x00\x00\x00\x00\x01\x00\x0C\x00\x6A\xFC')
        reply_details = bytearray(b'\x71\x00\x72\x00\x73\x00\x74\x00\x75\x00\x76\x00')
        reply_footer = bytearray(b'\x4B\xFD\x5C')
        reply = reply_header + reply_details + reply_footer

        expected_mi = [113, 114, 115, 116, 117, 118]

        requests = self._command.parse_reply(reply)
        actual_mi = requests[0].values

        self.assertListEqual(expected_mi, actual_mi)

    def test_parse_complex(self):
        self._init_example_complex()
        reply_header = bytearray(
            b'\x2F\x5F\x4F\x50\x4C\x43\xFE\x00\x01\x01\x00\x00\xCD\x00\x00\x00\x00\x00\x16\x00\x8C\x00\xD5\xFB')
        reply_details = bytearray(
            b'\x6b\x00\x00\x00\xf9\x03\xfb\x03\xfe\x03\xff\x03\x00\x04\x01\x04\xea\x07\xeb\x07'
            b'\x07\xa9\x0a\x00\x07\xa9\x07\xa9\x07\xa9\x07\xa9\x0a\x00\x00\x00\x00\x00\x00\x00'
            b'\x32\x01\x00\x00'
            b'\x32\x01\x00\x00'
            b'\xf4\x01\x00\x00'
            b'\xf4\x01\x00\x00'
            b'\x32\x01\x00\x00'
            b'\x32\x01\x00\x00'
            b'\x32\x01\x00\x00'
            b'\x32\x01\x00\x00'
            b'\x32\x01\x00\x00'
            b'\x32\x01\x00\x00'
            b'\xf4\x01\x00\x00'
            b'\xf4\x01\x00\x00'
            b'\xf4\x01\x00\x00\xf4\x01\x00'
            b'\x00\xf4\x01\x00\x00\xf4\x01\x00\x00\x49\xf4\x10\x00\x70\x00\x00\x00\x71\x00\x00\x00\xca\x35\x3a\x42'
            b'\x85\x42\x33\x33\x6a'
            b'\xc5\x3d\x82\x5d\x47\x4d\xd5\x48\x40\xc3\xf5\xf6\x45\x33\x97')
        reply_footer = bytearray(b'\x19\xe0\x5c')
        reply = reply_header + reply_details + reply_footer

        self._command.parse_reply(reply)

        self._assert_request_values_equal(0, [True])
        self._assert_request_values_equal(1, [True, False, True, False, True, True])
        self._assert_request_values_equal(2, [False, False, False, False, False, False, False, False, False])
        self._assert_request_values_equal(3, [False])
        self._assert_request_values_equal(4, [False, False])
        self._assert_request_values_equal(5, [False, False, False, False, False, False])
        self._assert_request_values_equal(6, [False])
        self._assert_request_values_equal(7, [False, False, False, False])
        self._assert_request_values_equal(8, [1017, 1019])
        self._assert_request_values_equal(9, [1022, 1023, 1024, 1025, 2026, 2027])
        self._assert_request_values_equal(10, [306, 306])
        self._assert_request_values_equal(11, [500, 500])
        self._assert_request_values_equal(12, [306, 306, 306, 306, 306, 306])
        self._assert_request_values_equal(13, [500, 500, 500, 500, 500, 500])
        self._assert_request_values_equal(14, [1111113])
        self._assert_request_values_equal(15, [112, 113, 1111111114])
        self._assert_request_values_equal(16, [43271])
        self._assert_request_values_equal(17, [10])
        self._assert_request_values_equal(18, [43271, 43271, 43271, 43271])
        self._assert_request_values_equal(19, [10, 0, 0, 0])
        self._assert_request_values_equal(20, [66.6])
        self._assert_request_values_equal(21, [-3752.14, 56789.3, 3.14, 7890.9])

    def _assert_request_values_equal(self, index, expected):
        actual = [round(v, 2) if isinstance(v, float) else v for v in self._requests[index].values]
        self.assertListEqual(expected, actual)

    def _init_example_1(self):
        """Example 1 in doc"""
        request = operand_request.MB(addresses=[1])
        self._command.add_request(request)

    def _init_example_2(self):
        """Example 2 in doc"""
        self._command.add_request(operand_request.MF(addresses=[15]))
        self._command.add_request(operand_request.MI(addresses=[1, 2, 3]))
        self._command.add_request(operand_request.MB(addresses=[1, 2, 3, 4, 5, 6, 7]))

    def _init_example_3(self):
        """Example 3 in doc"""
        self._command.add_request(operand_request.MB(addresses=[1, 2, 3, 4, 5, 6]))
        self._command.add_request(operand_request.MI(addresses=[6, 7, 8]))

    def _init_example_4(self):
        """Example 4 in doc"""
        self._command.add_request(operand_request.MI(addresses=[13], length=6))

    def _init_example_complex(self):
        """Example in doc appendix 1"""
        self._requests = [
            operand_request.MB(addresses=[78]),
            operand_request.MB(addresses=[34], length=6),
            operand_request.Input(addresses=[7], length=9),
            operand_request.Input(addresses=[65]),
            operand_request.TimerRunBit(addresses=[34, 129]),
            operand_request.TimerRunBit(addresses=[42], length=6),
            operand_request.CounterRunBit(addresses=[15]),
            operand_request.CounterRunBit(addresses=[6], length=4),
            operand_request.MI(addresses=[17, 19]),
            operand_request.MI(addresses=[1022], length=6),
            operand_request.TimerCurrent(addresses=[34, 129]),
            operand_request.TimerPreset(addresses=[34, 129]),
            operand_request.TimerCurrent(addresses=[42], length=6),
            operand_request.TimerPreset(addresses=[42], length=6),
            operand_request.ML(addresses=[13]),
            operand_request.DW(addresses=[12], length=3),
            operand_request.CounterCurrent(addresses=[15]),
            operand_request.CounterPreset(addresses=[15]),
            operand_request.CounterCurrent(addresses=[6], length=4),
            operand_request.CounterPreset(addresses=[6], length=4),
            operand_request.MF(addresses=[6]),
            operand_request.MF(addresses=[9], length=4)
        ]
        for request in self._requests:
            self._command.add_request(request)

    def assert_command(self, expected_bytes):
        actual = self._command.get_bytes()
        self.assert_bytes_equal(expected_bytes, actual)

    def assert_bytes_equal(self, expected, actual):
        def format_hex(c):
            return hex(c)[2:].zfill(2)

        expected = [format_hex(c) for c in expected]
        actual = [format_hex(c) for c in actual]
        try:
            self.assertEqual(expected, actual)
        except AssertionError:
            if len(expected) > len(actual):
                longest = expected
                other = actual
            else:
                longest = actual
                other = expected
            positions = [' '] * len(longest) * (6 + 2)
            for i in range(len(longest)):
                if i >= len(other) or longest[i] != other[i]:
                    positions[i * 6 + 2] = '^'
            positions = ''.join(positions)
            message = "\nExpected : %s\nActual   : %s\n           %s\nActual not equal to expected." % (
                expected, actual, positions)
            self.fail(message)
