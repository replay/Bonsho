import unittest
import calendar
import time
import datetime
from unittest import mock
from lib import utils
import queue
from clients.blockcypher import crawler


class CrawlerTest(unittest.TestCase):

    def setUp(self):
        self.queue = queue.Queue()
        self.crawler = crawler.Crawler(
            msg_queue=self.queue)

    def _stub_transaction_dict(self, values):
        '''Generate a stub transaction based on given values, blockcypher format'''
        return {
            'hash': values['hash'],
            'tx': [{
                'out': [
                    {'value': output['value'],
                     'addr': output['addr']}
                    for output in transaction['outputs']],
                'inputs': [
                    {'prev_out': {
                        'value': input['value'],
                        'addr': input['addr']}}
                    for input in transaction['inputs']],
            }
            for transaction in values['transactions']]}

    def _stub_block_dict(self, values):
        '''Generate a stub block based on given values, blockcypher format'''
        datestring = datetime.datetime.fromtimestamp(values['time'])
        return {
            'prev_block': values['prev_block'],
            'hash': values['hash'],
            'time': utils.Utils.utc_ts_to_str(
                values['time'],
                self.crawler.time_format),
            'txids': values['transaction_ids']}

    @mock.patch('requests.get', autospec=True)
    def test_get_transactions_by_age(self, requests_get):
        self.setUp()
        stub_head = mock.MagicMock()
        stub_head.json.return_value = {'hash': 'testhash1'}
        stub_transaction1 = mock.MagicMock()
        stub_transaction1.json.return_value = self._stub_transaction_dict({
            'hash': 'transaction1',
            'transactions': [{
                'outputs': [
                    {'value': 10, 'addr': 'addr1'},
                    {'value': 20, 'addr': 'addr2'}],
                'inputs': [
                    {'value': 30, 'addr': 'addr3'},
                    {'value': 40, 'addr': 'addr4'}]}]})

        stub_block1 = self._stub_block_dict({
            'prev_block': 'block0',
            'hash': 'block1',
            'time': calendar.timegm(time.gmtime()) - 400,
            'transaction_ids': [
                'transaction1',
                'transaction2']})

        stub_block2 = self._stub_block_dict({
            'prev_block': 'block1',
            'hash': 'block2',
            'time': calendar.timegm(time.gmtime()) - 2000,
            'transaction_ids': [
                'transaction1',
                'transaction2']})

        requests_get.side_effect = [
            stub_head,
            stub_block1,
            stub_block2]
