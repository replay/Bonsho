from clients.base import listener
from clients.blockchain_info import parser
from lib import connection
import json


class Listener(listener.ListenerBase):

    endpoint_name = 'Bonsho'
    ping_msg = ''
    ping_interval = 20
    connection_class = connection.WebsocketsConnection
    parser = parser.Parser

    def _is_pong(self, msg):
        return False

    def extract_transations(self, data):
        return data

    def subscribe(self):
        pass
