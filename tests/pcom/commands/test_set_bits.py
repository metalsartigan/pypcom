from unittest import TestCase

from pcom.commands import SetBits


class TestSetBits(TestCase):
    def setUp(self):
        super().setUp()
        values = [True, False, False, True, False]
        self.command = SetBits(code=SetBits.MEMORY, address=32, values=values)

    def test_codes(self):
        values = [True, False, False, True, False]
        self.assertEqual('SA', SetBits(code=SetBits.OUTPUT, address=32, values=values).code)
        self.assertEqual('SB', SetBits(code=SetBits.MEMORY, address=32, values=values).code)
        self.assertEqual('SS', SetBits(code=SetBits.SYSTEM, address=32, values=values).code)

    def test_get_bytes(self):
        expected = bytearray(b'/00SB002005100100E\r')

        actual = self.command.get_bytes()
        self.assertEqual(expected, actual)

    def test_parse(self):
        buffer = bytearray(b'/A00SBF5\r')
        actual = self.command.parse_reply(buffer)
        self.assertTrue(actual)
