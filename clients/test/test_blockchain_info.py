import unittest
from unittest import mock
import pickle
from models import blockchain
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

    @mock.patch('requests.get', autospec=True)
    def test_get_block_by_hash(self, requests_get):
        block_json = {"tx": [], "time": 10, "prev_block": "prv"}
        mock_block = mock.MagicMock()
        mock_block.json.return_value = block_json
        requests_get.return_value = mock_block
        returned_block = self.client._get_block_by_hash('abc')
        self.assertEqual(
            block_json['tx'],
            [x for x in returned_block.transactions])
        self.assertEqual(block_json['time'], returned_block.time)
        self.assertEqual(block_json['prev_block'], returned_block.prev_block)

    @mock.patch(
        'clients.blockchain_info.BlockchainInfoClient._get_block_by_hash',
        autospec=True)
    @mock.patch('requests.get', autospec=True)
    def test_get_latest_block(self, requests_get, get_block_by_hash):
        # recreate self.client to mock _get_block_by_hash method
        self.setUp()
        chain_head_json = {'hash': 'testvalue'}
        mock_chain_head = mock.MagicMock()
        mock_chain_head.json.return_value = chain_head_json
        requests_get.return_value = mock_chain_head
        self.client._get_latest_block()
        get_block_by_hash.assert_called_once_with(
            self.client,
            chain_head_json['hash'])

    @mock.patch(
        'clients.blockchain_info.BlockchainInfoClient._get_block_by_hash',
        autospec=True)
    def test_get_prev_block(self, get_block_by_hash):
        # recreate self.client to mock _get_block_by_hash method
        self.setUp()
        prev_block_hash = 'testvalue'
        mock_block = mock.MagicMock()
        mock_block.prev_block = prev_block_hash
        self.client._get_prev_block(mock_block)
        get_block_by_hash.assert_called_once_with(
            self.client,
            prev_block_hash)

    @mock.patch(
        'clients.blockchain_info.BlockchainInfoClient._get_prev_block',
        autospec=True)
    @mock.patch(
        'clients.blockchain_info.BlockchainInfoClient._get_latest_block',
        autospec=True)
    def test_get_block_by_age(self, get_latest_block, get_prev_block):
        # recreate self.client to mock methods
        self.setUp()

        def mock_block_gen():
            age = 0
            while age < 100:
                age = age + 1
                mock_block = mock.MagicMock()
                mock_block.age = age
                yield mock_block

        blocks = [x for x in mock_block_gen()]

        get_latest_block.side_effect = blocks[:1]
        get_prev_block.side_effect = blocks[1:]
        blocks = [x.age for x in self.client._get_blocks_by_age(5)]
        self.assertEqual(blocks, [1, 2, 3, 4, 5])

    @mock.patch(
        'clients.blockchain_info.BlockchainInfoClient._get_blocks_by_age',
        autospec=True)
    def test_get_transactions_by_age(self, get_blocks_by_age):
        # recreate self.client to mock methods
        self.setUp()

        def mock_block_gen():
            transactions = 0
            steps = 5
            age = 0
            while age < 5:
                mock_block = mock.MagicMock()
                mock_block.transactions = range(
                    transactions,
                    transactions + steps)
                mock_block.age = age
                age = age + 1
                transactions = transactions + steps
                yield mock_block

        blocks = [x for x in mock_block_gen()]

        get_blocks_by_age.return_value = blocks
        transactions = [x for x in self.client.get_transactions_by_age(5)]
        self.assertEqual(transactions, [x for x in range(0,25)])
