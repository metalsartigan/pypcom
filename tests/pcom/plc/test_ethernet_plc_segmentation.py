import errno
import os
import socket

from unittest import TestCase
from unittest.mock import patch

from pcom import EthernetPlc
from pcom.errors import PComError
from pcom.plc.ethernet_command_wrapper import EthernetCommandWrapper
from tests.pcom.commands.mock_binary_command import MockBinaryCommand
from tests.pcom.commands.mock_ascii_command import MockAsciiCommand


@patch.object(socket.socket, 'close')
@patch.object(socket.socket, 'connect')
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

        res = self._plc.send(command)

        self.assertEqual(bytearray(b'/A\x02\x03\x0409\r'), res)

    def test_recv_segmentation_ascii_timeout(self, mock_recv, *args):
        command = MockAsciiCommand()
        segment1 = bytearray([6, 6, 6, 6, 6, 6, 6])
        command_bytes = command.get_ethernet_recv_bytes()
        mock_recv.side_effect = [
            segment1,
            command_bytes[:2],
            command_bytes[2:7],
            socket.timeout(os.strerror(errno.ETIMEDOUT))
        ]

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
        expected = bytearray(b'/_OPLC\xfe\x00\x01\x00\x00\x00\xc2\x00\x01\x02\x03\x04\x05\x06\x04\x00j\xfc\x10\x11\x02\x03\xda\xff\\')

        actual = self._plc.send(command)

        self.assertEqual(expected, actual)
