from unittest import TestCase

from pcom.errors import PComError
from tests.pcom.commands.mock_ascii_command import MockAsciiCommand


class TestAsciiCommand(TestCase):
    def setUp(self):
        super().setUp()
        self.command = MockAsciiCommand()

    def test_validate_frame(self):
        msg = '00MK345'
        frame = bytearray(('/A%s' % msg).encode())
        frame.extend(self.command.get_crc_bytes(msg))
        frame.append(0xd)

        self.command.parse_reply(frame)

    def test_validate_frame_wrong_stx(self):
        msg = '00MK345'
        frame = bytearray(('zA%s' % msg).encode())
        frame.extend(self.command.get_crc_bytes(msg))
        frame.append(0xd)

        with self.assertRaisesRegex(PComError, "STX"):
            self.command.parse_reply(frame)

    def test_validate_frame_wrong_plc_id(self):
        msg = '01MK345'
        frame = bytearray(('/A%s' % msg).encode())
        frame.extend(self.command.get_crc_bytes(msg))
        frame.append(0xd)

        with self.assertRaisesRegex(PComError, "PLC ID"):
            self.command.parse_reply(frame)

    def test_validate_frame_wrong_command_code(self):
        msg = '00ZZ345'
        frame = bytearray(('/A%s' % msg).encode())
        frame.extend(self.command.get_crc_bytes(msg))
        frame.append(0xd)

        with self.assertRaisesRegex(PComError, "Command Code"):
            self.command.parse_reply(frame)

    def test_validate_frame_wrong_etx(self):
        msg = '00MK345'
        frame = bytearray(('/A%s' % msg).encode())
        frame.extend(self.command.get_crc_bytes(msg))
        frame.append(0xe)

        with self.assertRaisesRegex(PComError, "ETX"):
            self.command.parse_reply(frame)

    def test_validate_frame_wrong_crc(self):
        msg = '00MK345'
        frame = bytearray(('/A%s' % msg).encode())
        frame.extend(bytearray([0, 0]))
        frame.append(0xd)

        with self.assertRaisesRegex(PComError, "CRC"):
            self.command.parse_reply(frame)
