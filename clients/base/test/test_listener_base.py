import unittest
import pickle
from clients.base import listener
import queue
from lib import connection
from unittest import mock


class ConnectionClass:

    def __init__(self, url=None):
        self.url = url
        self.connected = False

    def recv(self):
        return '{"action": "test"}'

    def send(self, msg):
        pass

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False


class Listener(listener.ListenerBase):
    ws_endpoint_url = 'testurl'
    endpoint_name = 'Test Endpoint'
    chain_head_url = 'https://test'
    block_url = 'https://test'
    ping_msg = 'ping msg'
    ping_interval = 20
    connection_class = ConnectionClass

    def __init__(self, *args, **kwargs):
        super(Listener, self).__init__(*args, **kwargs)
        self.parser = mock.MagicMock()
        setattr(self.parser, 'build_transaction', mock.MagicMock())
        self.parser.build_transaction.return_value = 'processed transaction'

    def _is_pong(self, data):
        return False

    def subscribe(self):
        pass

    def extract_transactions(self, msg):
        return msg


class ListenerBaseTest(unittest.TestCase):

    def setUp(self):
        self.test_queue = queue.Queue()
        self.client = Listener(
            connection_class=ConnectionClass,
            msg_queue=self.test_queue)

    def test_read_message(self):
        self.assertRaises(
            connection.NotConnectedException,
            self.client.read_message)
        self.client.connect()
        self.assertEqual(
            self.client.read_message(),
            '{"action": "test"}')

    def test_connect_disconnect(self):
        self.client.connect()
        self.assertTrue(self.client.connection.__class__ == ConnectionClass)
        self.assertEqual(self.client.connection.url, "testurl")
        self.assertEqual(self.client.connection.connected, True)
        self.client.disconnect()
        self.assertEqual(self.client.connection.connected, False)

    def test_handle_incoming_data(self):
        self.client.connect()
        self.client.handle_incoming_data()
        msg = self.test_queue.get()
        self.assertEqual(msg, pickle.dumps('processed transaction'))
        self.client.parser.build_transaction.assert_called_once_with(
            {'action': 'test'})
