from clients.base import listener
from clients.blockchain_info import parser
from lib import connection
import json


class Listener(listener.ListenerBase):
    ws_endpoint_url = 'wss://ws.blockchain.info/inv'
    endpoint_name = 'Blockchain Info'
    ping_msg = '{"op":"ping_block"}'
    ping_interval = 20
    connection_class = connection.WebsocketsConnection
    parser = parser.BlockchainInfoParser

    def extract_transaction_data(self, data):
        return data['x']

    def subscribe(self):
        subscription = {'op': 'unconfirmed_sub'}
        self.connection.send(
            json.dumps(subscription))

    def _is_pong(self, msg):
        if 'op' in msg and msg['op'] == 'block':
            return True
        return False
