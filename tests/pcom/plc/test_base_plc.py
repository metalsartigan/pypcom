from unittest import TestCase
from unittest.mock import patch, MagicMock

from pcom.errors import PComError
from tests.pcom.commands.mock_ascii_command import MockAsciiCommand
from .mock_plc import MockPlc


class TestBasePlc(TestCase):
    def setUp(self):
        super().setUp()
        self._plc = MockPlc()

    def test_context_mgmt(self):
        self._plc._connect = MagicMock(side_effect=self._plc._connect)
        self._plc._close = MagicMock(side_effect=self._plc._close)
        with self._plc:
            self._plc._connect.assert_called_once()
            self._plc._close.assert_not_called()
        self._plc._close.assert_called_once()

    @patch.object(MockPlc, '_send_bytes')
    @patch.object(MockPlc, '_receive_bytes')
    def test_send(self, mock_receive, mock_send):
        command = MockAsciiCommand()
        mock_receive.return_value = command.get_recv_bytes()
        reply = self._plc.send(command)
        mock_send.assert_called_once_with(bytearray([1, 2, 3, 4]))
        mock_receive.assert_called_once()
        self.assertEqual(bytearray(b'/A\x02\x03\x0409\r'), reply)

    def test_send_overflow(self):
        command = MockAsciiCommand()
        with patch.object(MockAsciiCommand, 'get_bytes', return_value=bytearray([0] * 1000)):
            with self.assertRaisesRegex(PComError, "The PLC cannot accept messages that are longer than 500 bytes."):
                self._plc.send(command)
