import json
from clients import client_base


class BlockchainInfoClient(client_base.ClientBase):
    endpoint_url = 'wss://ws.blockchain.info/inv'
    endpoint_name = 'Blockchain Info'
    ping_msg = '{"op":"ping_block"}'
    ping_interval = 20

    def subscribe(self, addr=None):
        print('bi subscribing {0}'.format(addr))
        self.connection.send(
            json.dumps({
                'op': 'addr_sub',
                'addr': addr}))

    def parse_msg(self, msg):
        msg = json.loads(msg)
        if msg['op'] == 'block':
            return 'got op block (ping reply)'
        return msg
