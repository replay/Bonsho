

class ClientManager:

    def __init__(self, socket):
        self.clients = []
        self.socket = socket

    def add_client(self, client):
        self.clients.append(client)

    def get_socket_handler_pairs(self):
        return [
            (x.get_connection().get_socket(), x.handle_event)
            for x in self.clients]

    def handle_event(self):
        pass
