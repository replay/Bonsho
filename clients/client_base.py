import abc
import json
import pickle
import asyncio
import threading
from models import transaction
from lib import connection
from multiprocessing import Pipe


class ClientBase(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def endpoint_url(self):
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

    @abc.abstractmethod
    def subscribe(self, address):
        '''Subscribe to the notifications we are interested in.'''
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
        return transaction.BTCTransactionAddress(
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
        self.connection = self.connection_class(url=self.endpoint_url)
        self.connection.connect()

    def disconnect(self):
        self.connection.disconnect()

    def handle_cmd(self):
        cmd = self.cmd_pipe[1].recv()
        if cmd == 'shutdown':
            self.connection.close()
            self.loop.stop()
        elif cmd[:9] == 'subscribe':
            self.subscribe(cmd.split(':')[1])

    def handle_event(self):
        msg = json.loads(self.read_message())
        if not self._is_pong(msg):
            data = self._build_transaction(
                self._extract_transaction_data(msg))
            self.msg_queue.put(pickle.dumps(data), block=True, timeout=3)
