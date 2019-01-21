from unittest import TestCase
from mock import patch

from pcom.commands.base_command import PROTOCOL_BINARY
from pcom.errors import PComError
from pcom.plc.ethernet_command_wrapper import EthernetCommandWrapper
from tests.pcom.commands.mock_ascii_command import MockAsciiCommand


class TestEthernetCommandWrapper(TestCase):
    def setUp(self):
        with patch.object(EthernetCommandWrapper, '_create_command_id', return_value=[31, 104]):
            self.wrapper = EthernetCommandWrapper(MockAsciiCommand())
        super().setUp()

    def test_get_bytes(self):
        expected = bytearray(b'\x1fhe\x00\x04\x00\x01\x02\x03\x04')
        actual = self.wrapper.get_bytes()
        self.assertEqual(expected, actual)

    def test_parse_reply(self):
        buffer = bytearray(b'\x1fhe\x00C\x00/A00MK10T2A00400431B00200248P00100315F03100003FT0102301023AB\r')
        actual = self.wrapper.parse_reply(buffer)
        expected = bytearray(b'10T2A00400431B00200248P00100315F03100003FT0102301023')
        self.assertEqual(expected, actual)

    def test_command_id(self):
        wrapper1 = EthernetCommandWrapper(MockAsciiCommand())
        wrapper2 = EthernetCommandWrapper(MockAsciiCommand())
        self.assertEqual(2, len(wrapper1.command_id))
        self.assertEqual(2, len(wrapper2.command_id))
        self.assertNotEqual(wrapper1.command_id, wrapper2.command_id)
        self.assertTrue(0 <= wrapper1.command_id[0] <= 99)
        self.assertTrue(0 <= wrapper1.command_id[1] <= 99)
        self.assertTrue(0 <= wrapper2.command_id[0] <= 99)
        self.assertTrue(0 <= wrapper2.command_id[1] <= 99)

    def test_header_check_wrong_command_id(self):
        reply = self.wrapper.base_command.get_ethernet_recv_bytes()
        reply[:2] = [1, 2]
        with self.assertRaisesRegex(PComError, "Ethernet header mismatch."):
            self.wrapper.parse_reply(reply)

    def test_header_check_wrong_protocol(self):
        reply = self.wrapper.base_command.get_ethernet_recv_bytes()
        reply[2] = PROTOCOL_BINARY
        with self.assertRaisesRegex(PComError, "Ethernet header mismatch."):
            self.wrapper.parse_reply(reply)
