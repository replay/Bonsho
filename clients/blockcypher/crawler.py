from clients.base import crawler as crawler_base
from clients.blockcypher import parser
import calendar
import datetime
import requests

class Crawler(crawler_base.CrawlerBase):
    chain_head_url = 'http://api.blockcypher.com/v1/btc/main'
    block_url = 'https://api.blockcypher.com/v1/btc/main/blocks/{block}'
    parser = parser.BlockCypherParser

    def prepare_time(self, time):
        return calendar.timegm(
            datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ').timetuple())

    def get_transaction(self, tx_id):
        transaction_url = 'https://api.blockcypher.com/v1/btc/main/txs/{tx_id}'
        tx_data = requests.get(transaction_url.format(tx_id=tx_id)).json()
        return self.parser.build_transaction(tx_data)

    def prepare_transaction(self, txid):
        return self.get_transaction(txid)
