import unittest
from unittest import mock
from collections import deque
from clients.blockchain_info import crawler


class CrawlerTest(unittest.TestCase):

    def setUp(self):
        queue = deque()
        self.crawler = crawler.Crawler(
            connection_class=None,
            msg_queue=queue)

    @mock.patch('requests.get', autospec=True)
    def test_get_block_by_hash(self, requests_get):
        block_json = {"tx": [], "time": 10, "prev_block": "prv"}
        mock_block = mock.MagicMock()
        mock_block.json.return_value = block_json
        requests_get.return_value = mock_block
        returned_block = self.crawler.get_block_by_hash('abc')
        self.assertEqual(
            block_json['tx'],
            [x for x in returned_block.transactions])
        self.assertEqual(block_json['time'], returned_block.time)
        self.assertEqual(block_json['prev_block'], returned_block.prev_block)

    @mock.patch(
        'clients.blockchain_info.crawler.Crawler.get_block_by_hash',
        autospec=True)
    @mock.patch('requests.get', autospec=True)
    def test_get_latest_block(self, requests_get, get_block_by_hash):
        # recreate self.crawler to mock get_block_by_hash method
        self.setUp()
        chain_head_json = {'hash': 'testvalue'}
        mock_chain_head = mock.MagicMock()
        mock_chain_head.json.return_value = chain_head_json
        requests_get.return_value = mock_chain_head
        self.crawler.get_latest_block()
        get_block_by_hash.assert_called_once_with(
            self.crawler,
            chain_head_json['hash'])

    @mock.patch(
        'clients.blockchain_info.crawler.Crawler.get_block_by_hash',
        autospec=True)
    def test_get_prev_block(self, get_block_by_hash):
        # recreate self.crawler to mock get_block_by_hash method
        self.setUp()
        prev_block_hash = 'testvalue'
        mock_block = mock.MagicMock()
        mock_block.prev_block = prev_block_hash
        self.crawler.get_prev_block(mock_block)
        get_block_by_hash.assert_called_once_with(
            self.crawler,
            prev_block_hash)

    @mock.patch(
        'clients.blockchain_info.crawler.Crawler.get_prev_block',
        autospec=True)
    @mock.patch(
        'clients.blockchain_info.crawler.Crawler.get_latest_block',
        autospec=True)
    def test_get_block_by_age(self, get_latest_block, get_prev_block):
        # recreate self.crawler to mock methods
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
        blocks = [x.age for x in self.crawler.get_blocks_by_age(5)]
        self.assertEqual(blocks, [1, 2, 3, 4, 5])

    @mock.patch(
        'clients.blockchain_info.crawler.Crawler.get_blocks_by_age',
        autospec=True)
    def test_get_transactions_by_age(self, get_blocks_by_age):
        # recreate self.crawler to mock methods
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
        transactions = [x for x in self.crawler.get_transactions_by_age(5)]
        self.assertEqual(transactions, [x for x in range(0, 25)])
