import unittest
import pickle
from models import blockchain
from clients.blockchain_info import parser


class ParserTest(unittest.TestCase):

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

    expected_tx = blockchain.BTCTransaction(
        outputs=blockchain.BTCTransactionOutputs(
            outputs=[
                blockchain.BTCTransactionOutput(
                    value=6500000,
                    addresses=[
                        blockchain.BTCTransactionAddress(
                            address='1dice7W2AicHosf5EL3GFDUVga7TgtPFn')]),
                blockchain.BTCTransactionOutput(
                    value=20986690,
                    addresses=[
                        blockchain.BTCTransactionAddress(
                            address='1Ewk9iKm5Hu8Lxq21CMamnaWG6d3NcUc3p')]),
                ]),
        inputs=blockchain.BTCTransactionInputs(
            inputs=[
                blockchain.BTCTransactionInput(
                    value=27496690,
                    addresses=[
                        blockchain.BTCTransactionAddress(
                            address='1Ewk9iKm5Hu8Lxq21CMamnaWG6d3NcUc3p')])]),
        hash='426ea994a05614abf88ed01fee485a85105e2a8fc3591de77d26e' +
             '47a383c7119',
    )

    def setUp(self):
        self.parser = parser.Parser

    def test_parse_msg(self):
        message_parsed = self.parser.build_transaction(self.test_message['x'])
        self.assertEqual(
            pickle.dumps(message_parsed),
            pickle.dumps(self.expected_tx))
