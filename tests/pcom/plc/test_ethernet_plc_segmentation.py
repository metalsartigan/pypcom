import errno
import os

from unittest import TestCase
from unittest.mock import patch

from pcom import EthernetPlc
from pcom.errors import PComError
from pcom.plc import ethernet_plc
from pcom.plc.ethernet_command_wrapper import EthernetCommandWrapper
from tests.pcom.commands.mock_binary_command import MockBinaryCommand
from tests.pcom.commands.mock_ascii_command import MockAsciiCommand


@patch.object(ethernet_plc.socket.socket, 'close', side_effect=ethernet_plc.socket.socket.close, autospec=True)
@patch.object(ethernet_plc.socket.socket, 'connect')
@patch.object(EthernetCommandWrapper, '_create_command_id', return_value=[31, 104])
@patch.object(EthernetPlc, '_send_bytes')
@patch.object(EthernetPlc, '_socket_recv')
class TestEthernetPlc(TestCase):
    def setUp(self):
        super().setUp()
        self._address = ('127.0.0.1', 1616)
        self._plc = EthernetPlc(address=self._address, timeout=10)

    def test_recv_segmentation_ascii(self, mock_recv, *args):
        command = MockAsciiCommand()
        segment1 = bytearray([6, 6, 6, 6, 6, 6, 6])
        command_bytes = command.get_ethernet_recv_bytes()
        mock_recv.side_effect = [
            segment1,
            command_bytes[:2],
            command_bytes[2:7],
            command_bytes[7:]
        ]

        with self._plc:
            res = self._plc.send(command)

        self.assertEqual(bytearray(b'\x02\x03\x04'), res)

    def test_recv_segmentation_ascii_timeout(self, mock_recv, *args):
        command = MockAsciiCommand()
        segment1 = bytearray([6, 6, 6, 6, 6, 6, 6])
        command_bytes = command.get_ethernet_recv_bytes()
        mock_recv.side_effect = [
            segment1,
            command_bytes[:2],
            command_bytes[2:7],
            ethernet_plc.socket.timeout(os.strerror(errno.ETIMEDOUT))
        ]

        with self._plc:
            with self.assertRaisesRegex(PComError, 'timed out'):
                self._plc.send(command)

    def test_recv_segmentation_binary(self, mock_recv, *args):
        command = MockBinaryCommand()
        segment1 = bytearray([6, 6, 6, 6, 6, 6, 6])
        command_bytes = command.get_ethernet_recv_bytes()
        mock_recv.side_effect = [
            segment1,
            command_bytes[:2],
            command_bytes[2:7],
            command_bytes[7:]
        ]
        expected = bytearray(b'\x10\x11\x02\x03')

        with self._plc:
            actual = self._plc.send(command)

        self.assertEqual(expected, actual)
