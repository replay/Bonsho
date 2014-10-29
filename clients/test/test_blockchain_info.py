import unittest
import pickle
from models import transaction
from collections import deque
from clients import blockchain_info


class BlockchainInfoClientTest(unittest.TestCase):

    test_message = {
        'op': 'utx',
        'x': {
            'time': 1414435735,
            'size': 258,
            'vout_sz': 2,
            'out': [{
                'type': 0,
                'addr_tag_link': 'http://satoshidice.com',
                'value': 6500000,
                'addr': '1dice7W2AicHosf5EL3GFDUVga7TgtPFn',
                'addr_tag': 'SatoshiDICE 36%'
            }, {
                'value': 20986690,
                'addr': '1Ewk9iKm5Hu8Lxq21CMamnaWG6d3NcUc3p',
                'type': 0}],
            'hash': '426ea994a05614abf88ed01fee485a85105e2a8fc3591de77d26e' +
                    '47a383c7119',
            'vin_sz': 1,
            'inputs': [{
                'prev_out': {
                    'value': 27496690,
                    'addr': '1Ewk9iKm5Hu8Lxq21CMamnaWG6d3NcUc3p',
                    'type': 0}}],
            'tx_index': 67752554,
            'relayed_by': '127.0.0.1',
            'lock_time': 'Unavailable'}}

    expected_tx = transaction.BTCTransaction(
        outputs=transaction.BTCTransactionOutputs(
            outputs=[
                transaction.BTCTransactionOutput(
                    value=6500000,
                    addresses=[
                        transaction.BTCTransactionAddress(
                            address='1dice7W2AicHosf5EL3GFDUVga7TgtPFn')]),
                transaction.BTCTransactionOutput(
                    value=20986690,
                    addresses=[
                        transaction.BTCTransactionAddress(
                            address='1Ewk9iKm5Hu8Lxq21CMamnaWG6d3NcUc3p')]),
                ]),
        inputs=transaction.BTCTransactionInputs(
            inputs=[
                transaction.BTCTransactionInput(
                    value=27496690,
                    addresses=[
                        transaction.BTCTransactionAddress(
                            address='1Ewk9iKm5Hu8Lxq21CMamnaWG6d3NcUc3p')])]),
        hash='426ea994a05614abf88ed01fee485a85105e2a8fc3591de77d26e' +
             '47a383c7119',
    )

    def setUp(self):
        queue = deque()
        self.client = blockchain_info.BlockchainInfoClient(
            connection_class=None,
            msg_queue=queue)

    def test_parse_msg(self):
        message_parsed = self.client._build_transaction(
            self.client._extract_transaction_data(
                self.test_message))
        self.assertEqual(
            pickle.dumps(message_parsed),
            pickle.dumps(self.expected_tx))