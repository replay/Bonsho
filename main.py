#!/usr/bin/env python


import event_loop
import connection
import socket
from clients import blockchain_info
from clients import manager as client_manager

conf_sock = socket.socket()
conf_sock.bind(('127.0.0.1', 5555))

bic = blockchain_info.BlockchainInfoClient(
    connection_class=connection.WebsocketsConnection)
bic.initialize()

client_manager = client_manager.ClientManager(socket=conf_sock)
client_manager.add_client(bic)

event_loop = event_loop.EventLoop()
event_loop.add_reader(conf_sock, client_manager.handle_event)

for sock, handler in client_manager.get_socket_handler_pairs():
    event_loop.add_reader(sock, handler)

event_loop.run()
