from unittest import TestCase

from pcom.commands import WriteIntegers


class TestWriteIntegers(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.command_mi = WriteIntegers(code=WriteIntegers.MI, address=32, values=[258, 772])
        cls.command_ml = WriteIntegers(code=WriteIntegers.ML, address=32, values=[287454020, 84281096])

        cls.command_dw = WriteIntegers(code=WriteIntegers.DW, address=22, values=[2, 3, 4])
        cls.command_si = WriteIntegers(code=WriteIntegers.SI, address=22, values=[2, 3, 4])
        cls.command_sl = WriteIntegers(code=WriteIntegers.SL, address=22, values=[2, 3, 4])
        cls.command_sdw = WriteIntegers(code=WriteIntegers.SDW, address=22, values=[2, 3, 4])

    def test_code(self):
        self.assertEqual('SW', self.command_mi.code)
        self.assertEqual('SNL', self.command_ml.code)
        self.assertEqual('SND', self.command_dw.code)
        self.assertEqual('SF', self.command_si.code)
        self.assertEqual('SNH', self.command_sl.code)
        self.assertEqual('SNJ', self.command_sdw.code)

    def test_get_bytes(self):
        self.assertEqual(bytearray(b'/00SW00200201020304B8\r'), self.command_mi.get_bytes())
        self.assertEqual(bytearray(b'/00SNL00200211223344050607089F\r'), self.command_ml.get_bytes())

    def test_parse_reply(self):
        self.assertEqual(bytearray(), self.command_mi.parse_reply(bytearray(b'/A00SW0A\r')))
        self.assertEqual(bytearray(), self.command_ml.parse_reply(bytearray(b'/A00SN01\r')))
