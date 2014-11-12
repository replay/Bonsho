from clients.base import crawler as crawler_base
from clients.blockchain_info import parser

class Crawler(crawler_base.CrawlerBase):
    blocks_api_url = 'https://blockchain.info/blocks/{ms}?format=json'
    chain_head_url = 'https://blockchain.info/latestblock'
    block_url = 'https://blockchain.info/rawblock/{block}'
    parser = parser.BlockchainInfoParser

    def prepare_time(self, time):
        return time

    def prepare_transaction(self, txid):
        return self.parser.build_transaction(txid)
