import abc


class ClientBase(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def endpoint_url(self):
        '''The url we want to connect to.'''
        pass

    @abc.abstractmethod
    def subscribe(self):
        '''Subscribe to the notifications we are interested in.'''
        pass

    @abc.abstractmethod
    def handle_event(self, msg):
        '''Handle an event that occured'''
        pass

    @classmethod
    def get_endpoint(cls):
        return cls.endpoint_url

    def __init__(self, *args, **kwargs):
        self.connection_class = kwargs['connection_class']

    def read_message(self):
        if not hasattr(self, 'connection'):
            return "not connected"
        return self.connection.recv()

    def connect(self):
        self.connection = self.connection_class(url=self.endpoint_url)
        self.connection.connect()

    def initialize(self):
        self.connect()

    def get_connection(self):
        return self.connection
