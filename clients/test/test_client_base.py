import unittest
import pickle
from clients import client_base
import queue
from lib import connection


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


class Client(client_base.ClientBase):
    ws_endpoint_url = 'testurl'
    endpoint_name = 'Test Endpoint'
    ping_msg = 'ping msg'
    ping_interval = 20
    connection_class = ConnectionClass

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self.got_test_string = False

    def subscribe(self):
        pass

    def _build_transaction(self, msg):
        return msg

    def _extract_transaction_data(self, msg):
        return msg

    def _is_pong(self, value):
        return False


class ClientBaseTest(unittest.TestCase):

    def setUp(self):
        self.test_queue = queue.Queue()
        self.client = Client(
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

    def test_handle_event(self):
        self.client.connect()
        self.client.handle_event()
        msg = self.test_queue.get()
        self.assertEqual(msg, pickle.dumps({"action": "test"}))
