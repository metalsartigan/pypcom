from unittest import TestCase

from pcom.commands import CommandID


class TestCommandID(TestCase):
    def setUp(self):
        super().setUp()
        self.command = CommandID(plc_id=0)

    def test_get_bytes(self):
        expected = b'/00IDED\r'
        actual = self.command.get_bytes()
        self.assertEqual(expected, actual)
