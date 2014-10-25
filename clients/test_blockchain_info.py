import unittest
from clients import blockchain_info


class BlockchainInfoClientTest(unittest.TestCase):

    def setUp(self):
        self.client = blockchain_info.BlockchainInfoClient(
            connection_class=None)

    def test_handle_event(self):
        pass
