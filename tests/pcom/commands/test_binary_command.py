from unittest import TestCase

from pcom.errors import PComError
from tests.pcom.commands.mock_binary_command import MockBinaryCommand


class TestBinaryCommand(TestCase):
    def setUp(self):
        super().setUp()
        self.command = MockBinaryCommand()

    def test_parse_reply(self):
        frame = bytearray(
            b'/_OPLC\xFE\x00\x01\x00\x00\x00\xc2\x00\x01\x02\x03\x04\x05\x06\x04\x00\x6a\xfc\x10\x11\x02\x03\xda\xff\x5c')
        expected = bytearray(b'\x10\x11\x02\x03')
        details = self.command.parse_reply(frame)

        self.assertEqual(expected, details)

    def test_validate_frame_wrong_stx(self):
        frame = bytearray(
            b'y_OPIDTV\xFE\x00\x01\x00\x00\x00\xc2\x00\x01\x02\x03\x04\x05\x06\x04\x00\x6a\xfc\x10\x11\x02\x03\xda\xff\x5c')
        with self.assertRaisesRegex(PComError, "STX"):
            self.command.parse_reply(frame)

    def test_validate_frame_wrong_header_crc(self):
        frame = bytearray(
            b'/_OPLC\xFE\x00\x01\x00\x00\x00\xc2\x00\x01\x02\x03\x04\x05\x06\x04\x00\x6a\xfd\x10\x11\x02\x03\xda\xff\x5c')
        with self.assertRaisesRegex(PComError, "CRC"):
            self.command.parse_reply(frame)

    def test_validate_frame_wrong_details_length_too_long(self):
        frame = bytearray(
            b'/_OPLC\xFE\x00\x01\x00\x00\x00\xc2\x00\x01\x02\x03\x04\x05\x06\x05\x00\x6a\xfc\x10\x11\x02\x03\xda\xff\x5c')
        with self.assertRaisesRegex(PComError, "length"):
            self.command.parse_reply(frame)

    def test_validate_frame_wrong_details_length_too_short(self):
        frame = bytearray(
            b'/_OPLC\xFE\x00\x01\x00\x00\x00\xc2\x00\x01\x02\x03\x04\x05\x06\x03\x00\x6a\xfc\x10\x11\x02\x03\xda\xff\x5c')
        with self.assertRaisesRegex(PComError, "length"):
            self.command.parse_reply(frame)

    def test_validate_frame_wrong_details_crc(self):
        frame = bytearray(
            b'/_OPLC\xFE\x00\x01\x00\x00\x00\xc2\x00\x01\x02\x03\x04\x05\x06\x04\x00\x6a\xfc\x10\x11\x02\x03\xda\xf1\x5c')
        with self.assertRaisesRegex(PComError, "CRC"):
            self.command.parse_reply(frame)

    def test_validate_frame_wrong_etx(self):
        frame = bytearray(
            b'/_OPLC\xFE\x00\x01\x00\x00\x00\xc2\x00\x01\x02\x03\x04\x05\x06\x04\x00\x6a\xfc\x10\x11\x02\x03\xda\xff\xbc')
        with self.assertRaisesRegex(PComError, "ETX"):
            self.command.parse_reply(frame)

    def test_validate_frame_wrong_canbus_id(self):
        frame = bytearray(
            b'/_OPLC\xFE\x01\x01\x00\x00\x00\xc2\x00\x01\x02\x03\x04\x05\x06\x04\x00\x6a\xfc\x10\x11\x02\x03\xda\xff\x5c')
        with self.assertRaisesRegex(PComError, "plc id"):
            self.command.parse_reply(frame)

    def test_validate_frame_wrong_reserved(self):
        frame = bytearray(
            b'/_OPLC\x66\x00\x01\x00\x00\x00\xc2\x00\x01\x02\x03\x04\x05\x06\x04\x00\x6a\xfc\x10\x11\x02\x03\xda\xff\x5c')
        with self.assertRaisesRegex(PComError, "plc id"):
            self.command.parse_reply(frame)

    def test_validate_frame_wrong_command_number(self):
        frame = bytearray(
            b'/_OPLC\xFE\x00\x01\x00\x00\x00\xc1\x00\x01\x02\x03\x04\x05\x06\x04\x00\x6a\xfc\x10\x11\x02\x03\xda\xff\x5c')
        with self.assertRaisesRegex(PComError, "command number"):
            self.command.parse_reply(frame)

    def test_to_little_endian(self):
        self.assertEqual([0, 0], self.command.to_little_endian(0))
        self.assertEqual([1, 0], self.command.to_little_endian(1))
        self.assertEqual([255, 0], self.command.to_little_endian(255))
        self.assertEqual([0, 1], self.command.to_little_endian(256))
        self.assertEqual([255, 255], self.command.to_little_endian(65535))
        self.assertEqual([0, 0], self.command.to_little_endian(65536), msg="Overflow should loop")

    def test_to_long_little_endian(self):
        self.assertEqual([0, 0, 0, 0], self.command.to_long_little_endian(0))
        self.assertEqual([1, 0, 0, 0], self.command.to_long_little_endian(1))
        self.assertEqual([255, 0, 0, 0], self.command.to_long_little_endian(255))
        self.assertEqual([0, 1, 0, 0], self.command.to_long_little_endian(256))
        self.assertEqual([255, 255, 0, 0], self.command.to_long_little_endian(65535))
        self.assertEqual([0, 0, 1, 0], self.command.to_long_little_endian(65536))
        self.assertEqual([255, 255, 255, 255], self.command.to_long_little_endian(4294967295))
        self.assertEqual([0, 0, 0, 0], self.command.to_long_little_endian(4294967296), msg="Overflow should loop")
