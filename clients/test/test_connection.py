import unittest
from unittest import mock
from lib import connection
import websocket


class WebsocketsConnectionTest(unittest.TestCase):

    def setUp(self):
        self.testurl = 'http://urlurlurl'
        self.connection = connection.WebsocketsConnection(url=self.testurl)

    @mock.patch('websocket.create_connection')
    def test_connect(self, mock_create_connection):
        self.connection.connect()
        mock_create_connection.assert_called_once_with(self.testurl)

    @mock.patch('websocket.create_connection')
    def test_close(self, mock_create_connection):
        self.connection.connect()
        self.connection.close()
        self.connection.connection.close.assert_called_once_with()

    @mock.patch('websocket.create_connection')
    def test_get_socket(self, mock_create_connection):
        self.connection.connect()
        socketvalue = 'socket'
        self.connection.connection.sock = socketvalue
        self.assertEqual(socketvalue, self.connection.get_socket())

    @mock.patch('websocket.create_connection')
    def test_send(self, mock_create_connection):
        self.connection.connect()
        msg_value = 'myvalue'
        self.connection.send(msg_value)
        self.connection.connection.send.assert_called_once_with(msg_value)

    @mock.patch('lib.connection.WebsocketsConnection.connect')
    def test_recv_exceptions(self, mock_connect):
        self.connection.connection = websocket._core.WebSocket()
        self.connection.recv()
        self.connection.connect.assert_called_once_with()

    @mock.patch('websocket.create_connection')
    def test_recv(self, mock_create_connection):
        self.connection.connect()
        recv_value = 'value returned by receive'
        self.connection.connection.recv = mock.MagicMock(
            return_value=recv_value)
        self.assertEqual(recv_value, self.connection.recv())
