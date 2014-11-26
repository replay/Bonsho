import unittest
import queue
from lib import address_filter
from utter_libs.models import blockchain


class CrawlerTest(unittest.TestCase):

    def setUp(self):
        self.in_q = queue.Queue()
        self.out_q = queue.Queue()
        self.address_filter = address_filter.AddressFilter(
            in_q=self.in_q,
            out_q=self.out_q)
        self.address_filter.run()

    def _get_mock_transaction(self, addresses):
        return blockchain.BTCTransaction(
            hash='',
            inputs=blockchain.BTCTransactionInputs(inputs=[]),
            outputs=blockchain.BTCTransactionOutputs(
                outputs=[
                    blockchain.BTCTransactionOutput(
                        value=0,
                        addresses=[
                            blockchain.BTCTransactionAddress(
                                address=address)])
                    for address in addresses]))

    def tearDown(self):
        self.address_filter.shutdown()

    def test_address_filtering(self):

        mock_transaction1 = self._get_mock_transaction([
            'addr1', 'addr2', 'addr3'])
        result = self.address_filter.process_q_msg(mock_transaction1)
        self.assertEqual(result, None)

        self.address_filter.add_address('addr1')
        result = self.address_filter.process_q_msg(mock_transaction1)
        self.assertEqual(result, mock_transaction1)

        self.address_filter.del_address('addr1')
        result = self.address_filter.process_q_msg(mock_transaction1)
        self.assertEqual(result, None)

        self.address_filter.add_address('all')
        result = self.address_filter.process_q_msg(mock_transaction1)
        self.assertEqual(result, mock_transaction1)
