#!/usr/bin/env python


from lib import deduplicator
from lib import config
from lib import address_filter
from lib import callback_executor
from control_api import server as control_server
import queue
from websockets_api import server as websockets_server
from clients.blockcypher import listener as bc_listener
from clients.blockchain_info import listener as bi_listener
from clients.blockcypher import crawler as bc_crawler
from clients.blockchain_info import crawler as bi_crawler
from clients import manager as client_manager


class Bonsho:
    client_classes = [
        bc_listener.Listener,
        bi_listener.Listener]

    def __init__(self):
        self.config = config.Configuration()['Main']
        self.q1 = queue.Queue()
        self.q2 = queue.Queue()
        self.q3 = queue.Queue()
        self.api = control_server.ApiServer()
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
        self.api.run()

    def shutdown(self):
        self.client_manager.shutdown()
        self.address_filter.shutdown()
        self.deduper.shutdown()
        self.callback_executor.shutdown()


class Crawler:
    client_classes = [
        bc_crawler.Crawler,
        bi_crawler.Crawler]

    def __init__(self):
        self.config = config.Configuration()['Crawler']
        self.q1 = queue.Queue()
        self.client_manager = client_manager.ClientManager(out_q=self.q1)
        for client_class in self.client_classes:
            self.client_manager.add_client(client_class)
        self.websockets_api = websockets_server.WebsocketsApi(in_q=self.q1)

    def run(self):
        self.websockets_api.run()
        self.client_manager.run_all()
