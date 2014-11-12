import json
import requests
import calendar
import datetime
from models import blockchain
from clients import client_base
from lib import connection
from lib import config


class BlockCypherClient(client_base.ClientBase):
    ws_endpoint_url = 'ws://socket.blockcypher.com/v1/btc/main'
    chain_head_url = 'http://api.blockcypher.com/v1/btc/main'
    block_url = 'https://api.blockcypher.com/v1/btc/main/blocks/{block}'
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

    def _extract_block_transactions(self, block):
        return block['txids']

    def _build_transaction_input(self, data):
        return blockchain.BTCTransactionInput(
            value=data['output_value'],
            addresses=[
                blockchain.BTCTransactionAddress(
                    address=address)
                for address in data['addresses']])

    def _build_transaction_inputs(self, data):
        return blockchain.BTCTransactionInputs(
            inputs=[
                self._build_transaction_input(input)
                for input in data])

    def _build_transaction_output(self, data):
        return blockchain.BTCTransactionOutput(
            value=data['value'],
            addresses=[
                blockchain.BTCTransactionAddress(
                    address=address)
                for address in data['addresses']])

    def _build_transaction_outputs(self, data):
        return blockchain.BTCTransactionOutputs(
            outputs=[
                self._build_transaction_output(output)
                for output in data])

    def _build_transaction(self, tx_data):
        return blockchain.BTCTransaction(
            outputs=self._build_transaction_outputs(tx_data['outputs']),
            inputs=self._build_transaction_inputs(tx_data['inputs']),
            hash=tx_data['hash'])

    def _get_transaction(self, tx_id):
        transaction_url = 'https://api.blockcypher.com/v1/btc/main/txs/{tx_id}'
        tx_data = requests.get(transaction_url.format(tx_id=tx_id)).json()
        return self._build_transaction(tx_data)

    def _prepare_time(self, time):
        return calendar.timegm(
            datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ').timetuple())

    def _prepare_transaction(self, txid):
        return self._get_transaction(txid)
