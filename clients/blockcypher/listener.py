from clients.base import listener
from clients.blockcypher import parser
from lib import connection
from lib import config
import json


class Listener(listener.ListenerBase):
    ws_endpoint_url = 'ws://socket.blockcypher.com/v1/btc/main'
    endpoint_name = 'Block Cypher'
    ping_msg = '{"event": "ping"}'
    ping_interval = 20
    connection_class = connection.WebsocketsConnection
    parser = parser.BlockCypherParser

    def __init__(self, *args, **kwargs):
        super(Listener, self).__init__(*args, **kwargs)
        self.config = config.Configuration()['BlockCypher']

    def extract_transaction_data(self, data):
        return data

    def subscribe(self):
        subscription = {'event': 'unconfirmed-tx',
                        'token': self.config['token']}
        self.connection.send(
            json.dumps(subscription))

    def _is_pong(self, msg):
        if 'event' in msg and msg['event'] == 'pong':
            return True
        return False
