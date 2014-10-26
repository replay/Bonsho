import websocket


class NotConnectedException(Exception):
    pass


class WebsocketsConnection:

    def __init__(self, *args, **kwargs):
        self.url = kwargs['url']

    def send(self, msg):
        self.connection.send(msg)

    def recv(self):
        try:
            return self.connection.recv()
        except (websocket._exceptions.WebSocketConnectionClosedException,
                websocket._exceptions.WebSocketTimeoutException):
            self.connect()

    def get_socket(self):
        return self.connection.sock

    def connect(self):
        self.connection = websocket.create_connection(self.url)
