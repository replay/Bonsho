import abc
import queue
import threading
import event_loop
import connection


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

    @abc.abstractmethod
    def subscribe(self, address):
        '''Subscribe to the notifications we are interested in.'''
        pass

    @abc.abstractmethod
    def parse_msg(self, msg):
        '''Parse an incoming message.'''
        pass

    def __init__(self, *args, **kwargs):
        self.connection_class = kwargs['connection_class']
        self.msg_queue = kwargs['msg_queue']
        self.worker = threading.Thread(
            name='Worker for {0}'.format(self.endpoint_name),
            target=self._run,
            daemon=False)
        self.loop = event_loop.EventLoop()

    def _run(self):
        self.connect()
        self.loop.add_reader(
            self.connection.get_socket(),
            self.handle_event)
        self.ping()
        self.loop.run()

    def ping(self):
        self.connection.send(self.ping_msg)
        self.loop.loop.call_later(self.ping_interval, self.ping)

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

    def handle_event(self):
        msg = self.parse_msg(self.read_message())
        try:
            self.msg_queue.put(msg, block=True, timeout=3)
        except queue.Full:
            print("queue is full")
