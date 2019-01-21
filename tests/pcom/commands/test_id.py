from unittest import TestCase

from pcom.commands import ID


class TestID(TestCase):
    def setUp(self):
        super().setUp()
        self.command = ID(plc_id=0)

    def test_get_bytes(self):
        expected = b'/00IDED\r'
        actual = self.command.get_bytes()
        self.assertEqual(expected, actual)
