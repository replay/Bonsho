import asyncio
import pickle
import threading
import json
from multiprocessing import Pipe
from lib import worker_thread


class ListenerBase(worker_thread.WorkerThread):

    def __init__(self, *args, **kwargs):
        self.msg_queue = kwargs['msg_queue']
        self.cmd_pipe = Pipe()
        self.loop = asyncio.new_event_loop()
        self.worker_method = self._run
        super(ListenerBase, self).__init__(*args, **kwargs)

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
            self.handle_incoming_data)

        # setup ping job
        self.ping()

        # subscribe to listen to transactions
        self.subscribe()

        # run the loop
        self.loop.run_forever()

    def get_cmd_pipe(self):
        return self.cmd_pipe[0]

    def join(self):
        self.worker.join()

    def ping(self):
        self.connection.send(self.ping_msg)
        self.loop.call_later(self.ping_interval, self.ping)

    def read_message(self):
        if not hasattr(self, 'connection'):
            raise connection.NotConnectedException()
        return self.connection.recv()

    def connect(self):
        self.connection = self.connection_class(url=self.ws_endpoint_url)
        self.connection.connect()

    def disconnect(self):
        self.connection.disconnect()

    def handle_cmd(self):
        cmd = self.cmd_pipe[1].recv()
        if cmd == 'shutdown':
            self.connection.close()
            self.loop.stop()

    def handle_incoming_data(self):
        msg = json.loads(self.read_message())
        tx_data = self.extract_transaction_data(msg)
        if not self._is_pong(msg):
            self.msg_queue.put(
                pickle.dumps(
                    self.parser.build_transaction(tx_data)
                ),
                block=True,
                timeout=3)
