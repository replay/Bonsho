import json
import unittest
from collections import deque
from clients import blockchain_info


class BlockchainInfoClientTest(unittest.TestCase):

    def setUp(self):
        queue = deque()
        self.client = blockchain_info.BlockchainInfoClient(
            connection_class=None,
            msg_queue=queue)

    def test_parse_msg(self):
        message_raw = {'op': 'test'}
        message_parsed = self.client.parse_msg(json.dumps(message_raw))
        self.assertEqual(message_raw, message_parsed)
