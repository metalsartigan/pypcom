from unittest import TestCase

from pcom.commands import SetRtc

from datetime import datetime


class TestSetRtc(TestCase):
    def setUp(self):
        super().setUp()
        self.command = SetRtc(value=datetime(2019, 1, 21, 16, 40, 45))

    def test_code(self):
        self.assertEqual('SC', self.command.code)

    def test_get_bytes(self):
        expected = bytearray(b'/00SC45401601210119B9\r')

        actual = self.command.get_bytes()
        self.assertEqual(expected, actual)

    def test_parse(self):
        buffer = bytearray(b'/A00SCF6\r')
        actual = self.command.parse_reply(buffer)
        self.assertTrue(actual)
