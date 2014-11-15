import unittest
import queue
from clients.blockchain_info import listener


class ListenerTest(unittest.TestCase):

    def setUp(self):
        self.test_queue = queue.Queue()
        self.listener = listener.Listener(msg_queue=self.test_queue)
