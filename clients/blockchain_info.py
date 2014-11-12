import json
from models import blockchain
from clients import client_base
from lib import connection


class BlockchainInfoClient(client_base.ClientBase):
    ws_endpoint_url = 'wss://ws.blockchain.info/inv'
    blocks_api_url = 'https://blockchain.info/blocks/{ms}?format=json'
    transactions_api_url = 'https://blockchain.info/rawblock/{block_hash}'
    chain_head_url = 'https://blockchain.info/latestblock'
    block_url = 'https://blockchain.info/rawblock/{block}'
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

    def _extract_block_transactions(self, block):
        return block['tx']

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

    def _prepare_time(self, time):
        return time

    def _prepare_transaction(self, txid):
        return self._build_transaction(txid)
