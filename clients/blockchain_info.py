import json
import time
import requests
from models import blockchain
from clients import client_base
from lib import connection


class BlockchainInfoClient(client_base.ClientBase):
    ws_endpoint_url = 'wss://ws.blockchain.info/inv'
    blocks_api_url = 'https://blockchain.info/blocks/{ms}?format=json'
    transactions_api_url = 'https://blockchain.info/rawblock/{block_hash}'
    endpoint_name = 'Blockchain Info'
    ping_msg = '{"op":"ping_block"}'
    ping_interval = 20
    connection_class = connection.WebsocketsConnection

    def subscribe(self):
        subscription = {'op': 'unconfirmed_sub'}
        self.connection.send(
            json.dumps(subscription))

    def _is_pong(self, msg):
        if 'op' in msg and msg['op'] == 'block':
            return True
        return False

    def _extract_transaction_data(self, data):
        return data['x']

    def _build_transaction_input(self, data):
        return blockchain.BTCTransactionInput(
            value=data['value'],
            addresses=[
                blockchain.BTCTransactionAddress(
                    address=data['addr'])])

    def _build_transaction_inputs(self, data):
        return blockchain.BTCTransactionInputs(
            inputs=[
                self._build_transaction_input(input['prev_out'])
                for input in data
                if 'prev_out' in input])

    def _build_transaction_output(self, data):
        print(data)
        return blockchain.BTCTransactionOutput(
            value=data['value'],
            addresses=[
                blockchain.BTCTransactionAddress(
                    address=data['addr'])])

    def _build_transaction_outputs(self, data):
        return blockchain.BTCTransactionOutputs(
            outputs=[
                self._build_transaction_output(output)
                for output in data])

    def _build_transaction(self, tx_data):
        return blockchain.BTCTransaction(
            outputs=self._build_transaction_outputs(tx_data['out']),
            inputs=self._build_transaction_inputs(tx_data['inputs']),
            hash=tx_data['hash'])

    def _build_block(self, data):
        def transaction_generator(transactions):
            for transaction in transactions:
                yield self._build_transaction(transaction)

        return blockchain.Block(
            transactions=transaction_generator(data['tx']),
            time=data['time'],
            prev_block=data['prev_block'])

    def _get_latest_block(self):
        chain_head_url = 'https://blockchain.info/latestblock'
        head = requests.get(chain_head_url).json()
        return self._get_block_by_hash(head['hash'])

    def _get_block_by_hash(self, block):
        block_url = 'https://blockchain.info/rawblock/{block}'
        block_data = requests.get(block_url.format(block=block)).json()
        return self._build_block(block_data)

    def _get_prev_block(self, block):
        return self._get_block_by_hash(block.prev_block)

    # generator that returns all blocks until a given age in seconds
    def _get_blocks_by_age(self, age):
        block = self._get_latest_block()
        while block.age <= age:
            import pdb
            pdb.set_trace()
            block = self._get_prev_block(block)
            yield block

    def get_transactions_by_age(self, age):
        for block in self._get_blocks_by_age(age):
            for transaction in block.transactions:
                yield transaction
