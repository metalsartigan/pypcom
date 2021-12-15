from pcom.commands import WriteFloats
from unittest import TestCase


class TestWriteFloats(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.command_mf = WriteFloats(address=32, values=[2.1, 3.1])

    def test_code(self):
        self.assertEqual('SNF', self.command_mf.code)

    def test_get_bytes(self):
        self.assertEqual(bytearray(b'/00SNF0020026666400666664046B3\r'), self.command_mf.get_bytes())

    def test_not_in_range(self):
        with self.assertRaises(ValueError):
            WriteFloats(address=32, values=[-1.19e+38])

        with self.assertRaises(ValueError):
            WriteFloats(address=32, values=[3.41e+38])

    def test_parse_reply(self):
        self.assertEqual(bytearray(), self.command_mf.parse_reply(bytearray(b'/A00SN01\r')))
