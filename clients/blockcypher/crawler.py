from clients.base import crawler as crawler_base
from clients.blockcypher import parser
import calendar
import datetime
import requests


class Crawler(crawler_base.CrawlerBase):
    chain_head_url = 'http://api.blockcypher.com/v1/btc/main'
    block_url = 'https://api.blockcypher.com/v1/btc/main/blocks/{block}'
    transaction_url = 'https://api.blockcypher.com/v1/btc/main/txs/{tx_id}'
    parser = parser.BlockCypherParser
    time_format = '%Y-%m-%dT%H:%M:%SZ'

    def prepare_time(self, time):
        return calendar.timegm(
            datetime.datetime.strptime(time, self.time_format).timetuple())

    def get_transaction(self, tx_id):
        tx_data = requests.get(self.transaction_url.format(tx_id=tx_id)).json()
        return self.parser.build_transaction(tx_data)

    def prepare_transaction(self, txid):
        return self.get_transaction(txid)

    def extract_transactions(cls, block):
        return block['txids']
