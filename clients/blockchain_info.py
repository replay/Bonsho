from clients import client_base


class BlockchainInfoClient(client_base.ClientBase):
    endpoint_url = 'wss://ws.blockchain.info/inv'

    def subscribe(self, addr):
        self.connection.send('{"op":"addr_sub", "addr":"{0}"}'.format(addr))

    def handle_event(self):
        msg = self.read_message()
        print('received msg "{0}"'.format(msg))
