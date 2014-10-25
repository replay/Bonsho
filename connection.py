import websocket


class WebsocketsConnection:

    def __init__(self, *args, **kwargs):
        self.url = kwargs['url']

    def send(self, msg):
        self.connection.send(msg)

    def recv(self):
        return self.connection.recv()

    def get_socket(self):
        return self.connection.sock

    def connect(self):
        self.connection = websocket.create_connection(self.url)
