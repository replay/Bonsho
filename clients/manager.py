

class ClientManager:

    def __init__(self, socket):
        self.clients = []
        self.socket = socket

    def add_client(self, client):
        self.clients.append(client)

    def run_all(self):
        for client in self.clients:
            client.run()

    def subscribe_addresses(self, addresses):
        pass
