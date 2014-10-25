from clients import client_base


class BlockchainInfoClient(client_base.ClientBase):
    endpoint_url = 'wss://ws.blockchain.info/inv'

    def subscribe(self):
        self.connection.send('{"op":"unconfirmed_sub"}')

    def handle_event(self):
        msg = self.read_message()
        print('received msg "{0}"'.format(msg))
