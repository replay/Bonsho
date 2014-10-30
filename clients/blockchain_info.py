import json
from models import transaction
from clients import client_base
from lib import connection


class BlockchainInfoClient(client_base.ClientBase):
    endpoint_url = 'wss://ws.blockchain.info/inv'
    endpoint_name = 'Blockchain Info'
    ping_msg = '{"op":"ping_block"}'
    ping_interval = 20
    connection_class = connection.WebsocketsConnection

    def subscribe(self):
        subscription = {'op': 'unconfirmed_sub'}
        self.connection.send(
            json.dumps(subscription))

    def _is_pong(self, msg):
        if 'op' in msg.keys() and msg['op'] == 'block':
            return True
        return False

    def _extract_transaction_data(self, data):
        return data['x']

    def _build_transaction_input(self, data):
        return transaction.BTCTransactionInput(
            value=data['value'],
            addresses=[
                transaction.BTCTransactionAddress(
                    address=data['addr'])])

    def _build_transaction_inputs(self, data):
        return transaction.BTCTransactionInputs(
            inputs=[
                self._build_transaction_input(input['prev_out'])
                for input in data])

    def _build_transaction_output(self, data):
        return transaction.BTCTransactionOutput(
            value=data['value'],
            addresses=[
                transaction.BTCTransactionAddress(
                    address=data['addr'])])

    def _build_transaction_outputs(self, data):
        return transaction.BTCTransactionOutputs(
            outputs=[
                self._build_transaction_output(output)
                for output in data])

    def _build_transaction(self, tx_data):
        return transaction.BTCTransaction(
            outputs=self._build_transaction_outputs(tx_data['out']),
            inputs=self._build_transaction_inputs(tx_data['inputs']),
            hash=tx_data['hash'])


# The msg format we get from BlockchainInfo
'''
{'op': 'utx', 'x': {'time': 1414435735, 'size': 258, 'vout_sz': 2, 'out': [{'type': 0, 'addr_tag_link': 'http://satoshidice.com', 'value': 6500000, 'addr': '1dice7W2AicHosf5EL3GFDUVga7TgtPFn', 'addr_tag': 'SatoshiDICE 36%'}, {'value': 20986690, 'addr': '1Ewk9iKm5Hu8Lxq21CMamnaWG6d3NcUc3p', 'type': 0}], 'hash': '426ea994a05614abf88ed01fee485a85105e2a8fc3591de77d26e47a383c7119', 'vin_sz': 1, 'inputs': [{'prev_out': {'value': 27496690, 'addr': '1Ewk9iKm5Hu8Lxq21CMamnaWG6d3NcUc3p', 'type': 0}}], 'tx_index': 67752554, 'relayed_by': '127.0.0.1', 'lock_time': 'Unavailable'}} # noqa
'''
