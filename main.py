#!/usr/bin/env python


import event_loop
import connection
import socket
import deduplicator
import queue
from clients import blockchain_info
from clients import blockcypher
from clients import manager as client_manager

conf_sock = socket.socket()
conf_sock.bind(('127.0.0.1', 5555))

raw_q = queue.Queue()
deduplicated_q = queue.Queue()

bc = blockcypher.BlockCypherClient(
    connection_class=connection.WebsocketsConnection,
    msg_queue=raw_q)
bic = blockchain_info.BlockchainInfoClient(
    connection_class=connection.WebsocketsConnection,
    msg_queue=raw_q)

deduper = deduplicator.Deduplicator(
    in_q=raw_q,
    out_q=deduplicated_q)
deduper.process()

bc.initialize()
bic.initialize()

# these addresses are just to test, because they generate traffic
addresses = [
    '1VayNert3x1KzbpzMGt2qdqrAThiRovi8',
    '1dice7W2AicHosf5EL3GFDUVga7TgtPFn',
    '1dice6YgEVBf88erBFra9BHf6ZMoyvG88',
    '1dice97ECuByXAvqXpaYzSaQuPVvrtmz6',
    '1dice9wcMu5hLF4g81u8nioL5mmSHTApw',
    '1dice7fUkz5h4z2wPc1wLMPWgB5mDwKDx',
    '1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp',
    '1JH1hGjjB1J2u1cnkC6eUoqXnWHHnaSwvj',
    '1FhdCFvtRA3z92EoGz67Zer5LQxMG2TLud',
]

for addr in addresses:
    bc.subscribe(addr=addr)
    bic.subscribe(addr=addr)

client_manager = client_manager.ClientManager(socket=conf_sock)
client_manager.add_client(bic)
client_manager.add_client(bc)

event_loop = event_loop.EventLoop()
event_loop.add_reader(conf_sock, client_manager.handle_event)

for sock, handler in client_manager.get_socket_handler_pairs():
    event_loop.add_reader(sock, handler)

event_loop.run()
