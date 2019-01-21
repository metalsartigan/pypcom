from unittest import TestCase

from pcom.commands import CommandSetBits


class TestCommandSetBits(TestCase):
    def setUp(self):
        super().setUp()
        values = [True, False, False, True, False]
        self.command = CommandSetBits(code=CommandSetBits.MEMORY, address=32, values=values)

    def test_codes(self):
        values = [True, False, False, True, False]
        self.assertEqual('SA', CommandSetBits(code=CommandSetBits.OUTPUT, address=32, values=values).code)
        self.assertEqual('SB', CommandSetBits(code=CommandSetBits.MEMORY, address=32, values=values).code)
        self.assertEqual('SS', CommandSetBits(code=CommandSetBits.SYSTEM, address=32, values=values).code)

    def test_get_bytes(self):
        expected = bytearray(b'/00SB002005100100E\r')

        actual = self.command.get_bytes()
        self.assertEqual(expected, actual)

    def test_parse(self):
        buffer = bytearray(b'/A00SBF5\r')
        actual = self.command.parse_reply(buffer)
        self.assertTrue(actual)
