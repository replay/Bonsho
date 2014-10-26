import unittest
from clients import client_base
import queue


class Client(client_base.ClientBase):
    endpoint_url = 'testurl'
    endpoint_name = 'Test Endpoint'
    ping_msg = 'ping msg'

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self.got_test_string = False

    def subscribe(self):
        pass

    def parse_msg(self, msg):
        return msg


class ConnectionClass:

    def __init__(self, url=None):
        self.url = url
        self.connected = False

    def recv(self):
        return "teststring"

    def send(self, msg):
        pass

    def connect(self):
        self.connected = True


class ClientBaseTest(unittest.TestCase):

    def setUp(self):
        self.test_queue = queue.Queue()
        self.client = Client(
            connection_class=ConnectionClass,
            msg_queue=self.test_queue)

    def test_create_kill_pinger(self):
        self.assertFalse(self.client.has_pinger)
        self.client.connect()
        self.client.create_pinger()
        self.assertTrue(self.client.has_pinger)
        self.client.kill_pinger()
        self.assertFalse(self.client.has_pinger)

    def test_read_message(self):
        self.client.connection = ConnectionClass()
        self.assertEqual(self.client.read_message(), "teststring")

    def test_connect(self):
        self.client.connect()
        self.assertTrue(self.client.connection.__class__ == ConnectionClass)
        self.assertEqual(self.client.connection.url, "testurl")
        self.assertEqual(self.client.connection.connected, True)

    def test_initialize(self):
        self.client.initialize()
        self.assertTrue(self.client.connection.connected)
        self.assertTrue(self.client.has_pinger)
        self.client.kill_pinger()

    def test_get_connection(self):
        self.client.connect()
        connection = self.client.get_connection()
        self.assertTrue(connection.__class__ == ConnectionClass)

    def test_handle_event(self):
        self.client.handle_event()
        msg = self.test_queue.get()
        self.assertEqual(msg, 'not connected')
