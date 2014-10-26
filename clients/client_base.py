import abc
import queue
import pinger


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

    @abc.abstractmethod
    def subscribe(self, address):
        '''Subscribe to the notifications we are interested in.'''
        pass

    @abc.abstractmethod
    def parse_msg(self, msg):
        '''Parse an incoming message.'''
        pass

    @property
    def has_pinger(self):
        if (hasattr(self, 'ping_thread') and
            hasattr(self.ping_thread, 'worker') and
            hasattr(self.ping_thread.worker, 'isAlive')):
                return self.ping_thread.worker.isAlive()

    def __init__(self, *args, **kwargs):
        self.connection_class = kwargs['connection_class']
        self.msg_queue = kwargs['msg_queue']

    def create_pinger(self):
        self.ping_thread = pinger.Pinger(
            msg=self.ping_msg,
            endpoint=self.endpoint_name,
            connection=self.get_connection())

    def kill_pinger(self):
        self.ping_thread.send_quit()

    def read_message(self):
        if not hasattr(self, 'connection'):
            return "not connected"
        return self.connection.recv()

    def connect(self):
        self.connection = self.connection_class(url=self.endpoint_url)
        self.connection.connect()

    def initialize(self):
        self.connect()
        self.create_pinger()

    def get_connection(self):
        return self.connection

    def handle_event(self):
        msg = self.parse_msg(self.read_message())
        try:
            self.msg_queue.put(msg, block=True, timeout=3)
        except queue.Full:
            print("queue is full")
