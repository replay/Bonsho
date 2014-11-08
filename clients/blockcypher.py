import json
from models import transaction
from clients import client_base
from lib import connection
from lib import config


class BlockCypherClient(client_base.ClientBase):
    ws_endpoint_url = 'ws://socket.blockcypher.com/v1/btc/main'
    endpoint_name = 'Block Cypher'
    ping_msg = '{"event": "ping"}'
    ping_interval = 20
    connection_class = connection.WebsocketsConnection

    def __init__(self, *args, **kwargs):
        super(BlockCypherClient, self).__init__(*args, **kwargs)
        self.config = config.Configuration()['BlockCypher']

    def subscribe(self):
        subscription = {'event': 'unconfirmed-tx',
                        'token': self.config['token']}
        self.connection.send(
            json.dumps(subscription))

    def _is_pong(self, msg):
        if 'event' in msg and msg['event'] == 'pong':
            return True
        return False

    def _extract_transaction_data(self, data):
        return data

    def _build_transaction_input(self, data):
        return transaction.BTCTransactionInput(
            value=data['output_value'],
            addresses=[
                transaction.BTCTransactionAddress(
                    address=address)
                for address in data['addresses']])

    def _build_transaction_inputs(self, data):
        return transaction.BTCTransactionInputs(
            inputs=[
                self._build_transaction_input(input)
                for input in data])

    def _build_transaction_output(self, data):
        return transaction.BTCTransactionOutput(
            value=data['value'],
            addresses=[
                transaction.BTCTransactionAddress(
                    address=address)
                for address in data['addresses']])

    def _build_transaction_outputs(self, data):
        return transaction.BTCTransactionOutputs(
            outputs=[
                self._build_transaction_output(output)
                for output in data])

    def _build_transaction(self, tx_data):
        return transaction.BTCTransaction(
            outputs=self._build_transaction_outputs(tx_data['outputs']),
            inputs=self._build_transaction_inputs(tx_data['inputs']),
            hash=tx_data['hash'])

# The msg format we get from BlockCypher
'''
{'lock_time': 0, 'inputs': [{'output_value': 14185670, 'script': '493046022100fc66231576ca2a12b9914d6bd6fe45bcb265aecd232807d86e520668437306b4022100c43e8c64d20b881eac2f7069b6474ecf00cf3872aa59e127318566b530726740014104d087e1bb648bc101430a7e7d47d25f0110917788801079edce9b77a890e9a5fada14d7b73eea0d99a87e783deeaa966e74b8aa2fa5dbb50ce9894f51c268d1eb', 'prev_hash': '37a56074bc3764e925b9208fc8213d6fd67f6aac57370e69de3e048ed686262f', 'output_index': 1, 'addresses': ['1KiMNd5XxXHNYTbxdHsDEArZWzTFRKoxxy'], 'script_type': 'pay-to-pubkey-hash'}], 'hash': 'cbc3afa37a23daa14fc936987f1c605d120c3ea93990af6c8cd62a6e2898ba14', 'ver': 1, 'vout_sz': 2, 'block_height': -1, 'fees': 10000, 'relayed_by': '173.66.186.150:8333', 'addresses': ['1KiMNd5XxXHNYTbxdHsDEArZWzTFRKoxxy', '1boness9kPxgmRiKFZH9h9SZmuDJqjrQ9'], 'total': 14175670, 'confirmed': '1754-08-30T22:43:41.129Z', 'confirmations': 0, 'preference': 'medium', 'outputs': [{'script_type': 'pay-to-pubkey-hash', 'script': '76a914069532d8f65ea0624ddbb2cbcb3d597cc931e26688ac', 'spent_by': '', 'addresses': ['1boness9kPxgmRiKFZH9h9SZmuDJqjrQ9'], 'value': 1200000}, {'script_type': 'pay-to-pubkey-hash', 'script': '76a914cd44532c32748b8d8332efed5a39a96d54f36bee88ac', 'spent_by': '', 'addresses': ['1KiMNd5XxXHNYTbxdHsDEArZWzTFRKoxxy'], 'value': 12975670}], 'vin_sz': 1, 'double_spend': False, 'received': '2014-10-27T23:04:22.908Z'} # noqa
'''
