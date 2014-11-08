#!/usr/bin/env python


from lib import deduplicator
from lib import config
from lib import address_filter
from lib import callback_executor
import queue
from api import server
from clients import blockcypher
from clients import blockchain_info
from clients import manager as client_manager


# these addresses are just to test, because they generate traffic
addresses = [
    '1VayNert3x1KzbpzMGt2qdqrAThiRovi8',
    '1JH1hGjjB1J2u1cnkC6eUoqXnWHHnaSwvj',
    '1FhdCFvtRA3z92EoGz67Zer5LQxMG2TLud',
    '1dice9wVtrKZTBbAZqz1XiTmboYyvpD3t',
    '1dicegEArYHgbwQZhvr5G9Ah2s7SFuW1y',
    '1dicec9k7KpmQaA8Uc8aCCxfWnwEWzpXE',
    '1dice9wcMu5hLF4g81u8nioL5mmSHTApw',
    '1dice97ECuByXAvqXpaYzSaQuPVvrtmz6',
    '1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp',
    '1dice7W2AicHosf5EL3GFDUVga7TgtPFn',
    '1dice7fUkz5h4z2wPc1wLMPWgB5mDwKDx',
    '1dice7EYzJag7SxkdKXLr8Jn14WUb3Cf1',
    '1dice6YgEVBf88erBFra9BHf6ZMoyvG88',
    '1dice6wBxymYi3t94heUAG6MpG5eceLG1',
    '1dice6GV5Rz2iaifPvX7RMjfhaNPC8SXH',
    '1dice6gJgPDYz8PLQyJb8cgPBnmWqCSuF',
    '1dice6DPtUMBpWgv8i4pG8HMjXv9qDJWN',
]


class Bonsho:
    client_classes = [
        blockcypher.BlockCypherClient,
        blockchain_info.BlockchainInfoClient]

    def __init__(self):
        self.config = config.Configuration()['Main']
        self.q1 = queue.Queue()
        self.q2 = queue.Queue()
        self.q3 = queue.Queue()
        self.api = server.ApiServer()
        self.client_manager = client_manager.ClientManager(out_q=self.q1)
        for client_class in self.client_classes:
            self.client_manager.add_client(client_class)
        self.address_filter = address_filter.AddressFilter(
            in_q=self.q1,
            out_q=self.q2)
        self.deduper = deduplicator.Deduplicator(
            in_q=self.q2,
            out_q=self.q3)
        self.callback_executor = callback_executor.CallbackExecutor(
            in_q=self.q3)

    def run(self):
        self.callback_executor.run()
        self.deduper.run()
        self.address_filter.run()
        self.client_manager.run_all()
        self.client_manager.subscribe()
        self.api.run()

    def shutdown(self):
        self.client_manager.shutdown()
        self.address_filter.shutdown()
        self.deduper.shutdown()
        self.callback_executor.shutdown()


class Crawler:
    client_classes = [
        blockcypher.BlockCypherClient,
        blockchain_info.BlockchainInfoClient]

    def __init__(self):
        self.config = config.Configuration()['Crawler']
