import websockets
import asyncio
import pickle
from multiprocessing import Pipe
from lib import queue_filter_base
from lib import worker_thread


class WebsocketsServer(worker_thread.WorkerThread):

    def __init__(self):
        self.running = False
        self.conn_queues = []
        self.worker_method = self._run
        self.pipe = Pipe()
        super(WebsocketsServer, self).__init__(self)
        self.server = websockets.serve(self.new_conn, 'localhost', 8765)

    def _run(self):
        '''Setup the event loop'''
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().add_reader(
            self.pipe[1],
            self.send_to_all)
        self.running = True
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    def get_input_pipe(self):
        return self.pipe[0]

    @asyncio.coroutine
    def new_conn(self, websocket, path):
        '''creates a queue for each new connection, listens to it, and
           forwards all the data it's getting from the queue'''
        conn_q = asyncio.Queue()
        self.conn_queues.append(conn_q)
        while True:
            message = yield from conn_q.get()
            if not websocket.open:
                self.conn_queues.remove(conn_q)
                break
            yield from websocket.send(message)

    def send_to_all(self):
        '''Send data from input pipe to all connections'''
        data = self.pipe[1].recv()
        if data == 'shutdown':
            asyncio.get_event_loop().stop()
        for queue in self.conn_queues:
            asyncio.get_event_loop().create_task(queue.put(data))

    def shutdown(self):
        self.server.close()
        self.get_input_pipe().send('shutdown')


class WebsocketsApi(queue_filter_base.QueueFilterBase):

    def __init__(self, *args, **kwargs):
        super(WebsocketsApi, self).__init__(*args, **kwargs)
        self.ws_server = WebsocketsServer()
        self.output_pipe = self.ws_server.get_input_pipe()
        self.ws_server.run()

    def process_q_msg(self, transaction):
        self.output_pipe.send(pickle.dumps(transaction))

    def shutdown(self):
        self.ws_server.shutdown()
        super(WebsocketsApi, self).shutdown()
