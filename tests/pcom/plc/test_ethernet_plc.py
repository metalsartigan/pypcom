import errno
import os
import socket

from unittest import TestCase
from unittest.mock import patch

from pcom import EthernetPlc
from pcom.errors import PComError
from pcom.plc.ethernet_command_wrapper import EthernetCommandWrapper
from tests.pcom.commands.mock_ascii_command import MockAsciiCommand


@patch.object(socket.socket, 'close')
@patch.object(socket.socket, 'connect')
class TestEthernetPlc(TestCase):
    def setUp(self):
        super().setUp()
        self._address = ('127.0.0.1', 1616)
        self._plc = EthernetPlc(address=self._address, timeout=10)

    def test_connect(self, mock_connect, mock_close, *args):
        with self._plc:
            mock_connect.assert_called_once_with(self._address)
            mock_close.assert_not_called()
        mock_connect.assert_called_once()

    @patch.object(EthernetCommandWrapper, '_create_command_id', return_value=[31, 104])
    @patch.object(EthernetPlc, '_send_bytes')
    @patch.object(EthernetPlc, '_socket_recv')
    def test_send(self, mock_recv, mock_send, *args):
        command = MockAsciiCommand()
        mock_recv.return_value = command.get_ethernet_recv_bytes()
        wrapper = EthernetCommandWrapper(command)
        expected_send = wrapper.get_bytes()
        expected = bytearray(b'/A\x02\x03\x0409\r')

        actual = self._plc.send(command)

        mock_send.assert_called_once_with(expected_send)
        mock_recv.assert_called_once()

        self.assertEqual(expected, actual)

    def test_connect_timeout(self, mock_connect, *args):
        side_effect = TimeoutError(os.strerror(errno.ETIMEDOUT))
        self._assert_connection_error(mock_connect, side_effect, "Connection timed out")
        side_effect = socket.timeout(os.strerror(errno.ETIMEDOUT))
        self._assert_connection_error(mock_connect, side_effect, "Connection timed out")

    def test_connect_refused(self, mock_connect, *args):
        side_effect = ConnectionRefusedError(os.strerror(errno.ECONNREFUSED))
        self._assert_connection_error(mock_connect, side_effect, "Connection refused")

    def _assert_connection_error(self, mock_connect, side_effect, message, error_class=PComError):
        mock_connect.side_effect = side_effect
        with self.assertRaisesRegex(error_class, message):
            with self._plc:
                pass

    def test_connect_no_route_to_host(self, mock_connect, *args):
        side_effect = OSError(errno.EHOSTUNREACH, 'No route to host')
        self._assert_connection_error(mock_connect, side_effect, "No route to host")

    def test_connect_other_error(self, mock_connect, *args):
        side_effect = OSError(errno.ECHILD, 'Hey hey!')
        self._assert_connection_error(mock_connect, side_effect, "Hey hey!", OSError)

    @patch.object(EthernetPlc, '_send_bytes')
    @patch.object(EthernetPlc, '_socket_recv')
    def test_recv_timeout(self, mock_recv, *args):
        mock_recv.side_effect = socket.timeout(os.strerror(errno.ETIMEDOUT))
        command = MockAsciiCommand()
        with self.assertRaisesRegex(PComError, 'timed out'):
            self._plc.send(command)
