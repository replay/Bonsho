import websockets
import asyncio
from lib import queue_filter_base
from lib import worker_thread


class WebsocketsConnectionHandler(worker_thread.WorkerThread):
    pass


class WebsocketsApi(queue_filter_base.QueueFilterBase):

    def __init__(self, *args, **kwargs):
        self.connections = []
        super(WebsocketsApi, self).__init__(*args, **kwargs)
        start_server = websockets.serve('hello', 'localhost', 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    @asyncio.coroutine
    def new_connection(self, websocket, path):
        print('new connection')
        self.connections.append(websocket)

    def process_q_msg(self, transaction):
        print('sending transaction')
        for connection in self.connections:
            connection.send(transaction)
