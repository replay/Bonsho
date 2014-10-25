import unittest
from clients import client_base


class Client(client_base.ClientBase):
    endpoint_url = "testurl"

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)

    def subscribe(self):
        pass

    def handle_event(self):
        pass


class ConnectionClass:

    def __init__(self, url=None):
        self.url = url
        self.connected = False

    def recv(self):
        return "teststring"

    def connect(self):
        self.connected = True


class ClientBaseTest(unittest.TestCase):

    def setUp(self):
        self.client = Client(connection_class=ConnectionClass)

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

    def test_get_connection(self):
        self.client.connect()
        connection = self.client.get_connection()
        self.assertTrue(connection.__class__ == ConnectionClass)
