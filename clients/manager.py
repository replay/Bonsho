

class ClientManager:

    def __init__(self, socket):
        self.clients = []
        self.socket = socket

    def add_client(self, client):
        self.clients.append(client)

    def run_all(self):
        for client in self.clients:
            client.run()

    def send_to_all(self, cmd):
        for client in self.clients:
            client.get_cmd_pipe().send(cmd)

    def shutdown(self):
        self.send_to_all('shutdown')
        for client in self.clients:
            client.join()

    def subscribe_addresses(self, addresses):
        for address in addresses:
            self.send_to_all('subscribe:{address}'.format(
                address=address))
