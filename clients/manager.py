

class ClientManager:
    _instance = None

    def __init__(self, out_q):
        self.__class__._instance = self
        self.out_q = out_q
        self.clients = []

    @classmethod
    def get_instance(cls):
        return cls._instance

    def add_client(self, client_class):
        self.clients.append(
            client_class(msg_queue=self.out_q))

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

    def subscribe(self):
        self.send_to_all('subscribe')
