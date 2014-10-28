#!/usr/bin/env python


import connection
import socket
import deduplicator
import queue
import time
import logging
import asyncio
import conf_server
from clients import blockchain_info
from clients import blockcypher
from clients import manager as client_manager


conf_loop = asyncio.new_event_loop()
conf_s = conf_loop.create_server(conf_server.ConfServer, '127.0.0.1', 5555)

raw_q = queue.Queue()
unique_q = queue.Queue()

client_classes = [
    blockcypher.BlockCypherClient,
    blockchain_info.BlockchainInfoClient]

client_manager = client_manager.ClientManager()

for client_class in client_classes:
    client = client_class(
        connection_class=connection.WebsocketsConnection,
        msg_queue=raw_q)
    client_manager.add_client(client)

client_manager.run_all()

deduper = deduplicator.Deduplicator(
    in_q=raw_q,
    out_q=unique_q)
deduper.process()

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

client_manager.subscribe_addresses(addresses)

conf_loop.run_until_complete(conf_s)
conf_loop.run_forever()

client_manager.shutdown()
deduper.shutdown()
