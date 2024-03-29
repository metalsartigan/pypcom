from unittest import TestCase

from pcom.commands import ReadRtc
from datetime import datetime


class TestReadRtc(TestCase):
    def setUp(self):
        super().setUp()
        self.command = ReadRtc()

    def test_command_code(self):
        self.assertEqual('RC', self.command.code)

    def test_parse_reply(self):
        buffer = bytearray(b'/A00RC15081502210119B9\r')
        actual = self.command.parse_reply(buffer)
        expected = datetime(2019, 1, 21, 15, 8, 15)
        self.assertEqual(expected, actual)
