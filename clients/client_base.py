import abc
import requests
import json
import pickle
import asyncio
import threading
from models import blockchain
from lib import connection
from multiprocessing import Pipe


class ClientBase(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def ws_endpoint_url(self):
        '''The url we want to connect to.'''
        pass

    @property
    @abc.abstractmethod
    def ping_msg(self):
        '''Message that is used to ping endpoint.'''
        pass

    @property
    @abc.abstractmethod
    def endpoint_name(self):
        '''Each endpoint shall have a name.'''
        pass

    @property
    @abc.abstractmethod
    def ping_interval(self):
        '''Each x seconds a ping should be sent.'''
        pass

    @property
    @abc.abstractmethod
    def connection_class(self):
        pass

    @property
    @abc.abstractmethod
    def chain_head_url(self):
        pass

    @property
    @abc.abstractmethod
    def block_url(self):
        pass

    @abc.abstractmethod
    def _build_transaction(self, tx_data):
        '''Build Transaction object from data.'''
        pass

    @abc.abstractmethod
    def _extract_transaction_data(self, data):
        '''Extract transaction from raw data.'''
        pass

    @abc.abstractmethod
    def _is_pong(self, msg):
        '''Check if message is a ping reply.'''
        pass

    @abc.abstractmethod
    def _extract_block_transactions(self, block):
        pass

    @abc.abstractmethod
    def subscribe(self):
        '''Subscribe to the notifications we are interested in.'''
        pass

    @abc.abstractmethod
    def _prepare_time(self):
        pass

    @abc.abstractmethod
    def _prepare_transaction(self):
        pass

    def __init__(self, *args, **kwargs):
        self.msg_queue = kwargs['msg_queue']
        self.cmd_pipe = Pipe()
        self.loop = asyncio.new_event_loop()
        self.worker = threading.Thread(
            name='Worker for {0}'.format(self.endpoint_name),
            target=self._run,
            daemon=False)

    def _run(self):
        # setup command listener
        self.loop.add_reader(
            self.cmd_pipe[1],
            self.handle_cmd)

        # connect to api
        self.connect()

        # handle events coming from api
        self.loop.add_reader(
            self.connection.get_socket(),
            self.handle_event)

        # setup ping job
        self.ping()

        # run the loop
        self.loop.run_forever()

    def _build_address(self, address_dict):
        return blockchain.BTCTransactionAddress(
            address=address_dict['addr'],
            value=address_dict['value'])

    def join(self):
        self.worker.join()

    def get_cmd_pipe(self):
        return self.cmd_pipe[0]

    def ping(self):
        self.connection.send(self.ping_msg)
        self.loop.call_later(self.ping_interval, self.ping)

    def run(self):
        self.worker.start()

    def read_message(self):
        if not hasattr(self, 'connection'):
            raise connection.NotConnectedException()
        return self.connection.recv()

    def connect(self):
        self.connection = self.connection_class(url=self.ws_endpoint_url)
        self.connection.connect()

    def disconnect(self):
        self.connection.disconnect()

    def handle_cmd(self):
        cmd = self.cmd_pipe[1].recv()
        if cmd == 'shutdown':
            self.connection.close()
            self.loop.stop()
        elif cmd == 'subscribe':
            self.subscribe()

    def handle_event(self):
        msg = json.loads(self.read_message())
        if not self._is_pong(msg):
            data = self._build_transaction(
                self._extract_transaction_data(msg))
            self.msg_queue.put(pickle.dumps(data), block=True, timeout=3)

    def get_transactions_by_age(self, age):
        for block in self._get_blocks_by_age(age):
            for transaction in block.transactions:
                yield transaction

    def _get_blocks_by_age(self, age):
        block = self._get_latest_block()
        while block.age <= age:
            yield block
            block = self._get_prev_block(block)

    def _get_prev_block(self, block):
        return self._get_block_by_hash(block.prev_block)

    def _get_latest_block(self):
        head = requests.get(self.chain_head_url).json()
        return self._get_block_by_hash(head['hash'])

    def _get_block_by_hash(self, block):
        block_data = requests.get(self.block_url.format(block=block)).json()
        return self._build_block(block_data)

    def _build_block(self, data):
        timestamp = self._prepare_time(data['time'])

        def transaction_generator(transactions):
            for transaction in transactions:
                yield self._prepare_transaction(transaction)

        return blockchain.Block(
            transactions=transaction_generator(
                self._extract_block_transactions(data)),
            time=timestamp,
            prev_block=data['prev_block'])
