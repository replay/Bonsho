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

    def _build_block(self, data):
        timestamp = calendar.timegm(
            datetime.datetime.strptime(
                data['time'],
                '%Y-%m-%dT%H:%M:%SZ').timetuple())

        def transaction_generator(txids):
            for txid in txids:
                yield self._get_transaction(txid)

        return blockchain.Block(
            transactions=transaction_generator(data['txids']),
            time=timestamp,
            prev_block=data['prev_block'])

    def _get_latest_block(self):
        chain_head_url = 'http://api.blockcypher.com/v1/btc/main'
        head = requests.get(chain_head_url).json()
        return self._get_block_by_hash(head['hash'])

    def _get_block_by_hash(self, block):
        block_url = 'https://api.blockcypher.com/v1/btc/main/blocks/{block}'
        block = requests.get(block_url.format(block=block)).json()
        return self._build_block(block)

    def _get_prev_block(self, block):
        return self._get_block_by_hash(block.prev_block)

    def _get_transaction(self, tx_id):
        transaction_url = 'https://api.blockcypher.com/v1/btc/main/txs/{tx_id}'
        tx_data = requests.get(transaction_url.format(tx_id=tx_id)).json()
        return self._build_transaction(tx_data)

    # generator that returns all blocks until a given age in seconds
    def _get_blocks_by_age(self, age):
        block = self._get_latest_block()
        while block.age <= age:
            block = self._get_prev_block(block)
            yield block

    def get_transactions_by_age(self, age):
        for block in self._get_blocks_by_age(age):
            for transaction in block.transactions:
                yield transaction
