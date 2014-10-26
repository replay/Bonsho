import json
from clients import client_base


class BlockCypherClient(client_base.ClientBase):
    endpoint_url = 'ws://socket.blockcypher.com/v1/btc/main'
    endpoint_name = 'Block Cypher'
    ping_msg = '{ "event": "ping" }'
    ping_interval = 20

    def subscribe(self, addr=None):
        self.connection.send(
            json.dumps({
                'event': 'unconfirmed-tx',
                'address': addr}))

    def parse_msg(self, msg):
        msg = json.loads(msg)
        if msg['event'] == 'pong':
            return 'got pong'
        return msg
