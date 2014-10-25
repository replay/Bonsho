#!/usr/bin/env python


import event_loop
import connection
from clients import blockchain_info

bic = blockchain_info.BlockchainInfoClient(
    connection_class=connection.WebsocketsConnection)
event_loop = event_loop.EventLoop()
bic.initialize()
event_loop.add_reader(bic.get_connection(), bic.handle_event)
event_loop.run()
