import asyncio
import requests
import pickle
from utter_libs.models import blockchain
from lib import worker_thread


class CrawlerBase(worker_thread.WorkerThread):

    def __init__(self, *args, **kwargs):
        self.msg_queue = kwargs['msg_queue']
        self.loop = asyncio.new_event_loop()
        self.worker_method = self._run
        super(CrawlerBase, self).__init__(*args, **kwargs)

    def _run(self):
        self.crawl()
        self.loop.call_later(60, self._run)

    def crawl(self):
        for transaction in self.get_transactions_by_age(1200):
            self.msg_queue.put(
                pickle.dumps(transaction),
                block=True,
                timeout=3)

    def get_transactions_by_age(self, age):
        for block in self.get_blocks_by_age(age):
            for transaction in block.transactions:
                yield transaction

    def get_blocks_by_age(self, age):
        block = self.get_latest_block()
        while block.age <= age:
            yield block
            block = self.get_prev_block(block)

    def get_prev_block(self, block):
        return self.get_block_by_hash(block.prev_block)

    def get_latest_block(self):
        head = requests.get(self.chain_head_url).json()
        return self.get_block_by_hash(head['hash'])

    def get_block_by_hash(self, block):
        block_data = requests.get(self.block_url.format(block=block)).json()
        return self.build_block(block_data)

    def build_block(self, data):
        timestamp = self.prepare_time(data['time'])

        def transaction_generator(transactions):
            for transaction in transactions:
                yield self.prepare_transaction(transaction)

        return blockchain.Block(
            transactions=transaction_generator(
                self.extract_transactions(data)),
            time=timestamp,
            prev_block=data['prev_block'])
