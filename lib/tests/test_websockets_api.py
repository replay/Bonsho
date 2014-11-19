import unittest
import queue
import asyncio
import websockets
import pickle
import threading
from lib import websockets_api


class WebsocketsApiTest(unittest.TestCase):

    def setUp(self):
        self.queue = queue.Queue()
        self.api = websockets_api.WebsocketsApi(in_q=self.queue)

    def _connect(self, results, event):
        @asyncio.coroutine
        def get_data(results, event):
            websocket = yield from websockets.connect('ws://localhost:8765/')
            event.set()
            data = yield from websocket.recv()
            results.append(data)
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete(get_data(results, event))

    def _produce_data(self, events, data):
        for event in events:
            event.wait()
        self.queue.put(pickle.dumps(data))

    def test_connect_send_data(self):
        results = []
        threads = []
        events = []
        testdata = 'somestring123'
        num_conns = 50

        self.api.run()

        while not self.api.ws_server.running:
            pass

        for i in range(num_conns):
            event = threading.Event()
            events.append(event)
            threads.append(threading.Thread(
                target=self._connect, args=[results, event]))
        producer = threading.Thread(
            target=self._produce_data, args=[events, testdata])

        for thread in threads:
            thread.start()

        producer.start()

        for thread in threads:
            thread.join()

        producer.join()

        for i in range(num_conns):
            self.assertEqual(pickle.dumps(testdata), results[i])

        self.api.shutdown()
