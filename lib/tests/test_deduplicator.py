import unittest
from unittest import mock
import pickle
from lib import deduplicator
import queue


class TestClass:
    hash = 'sometesthash'


class DeduplicatorTest(unittest.TestCase):

    @mock.patch('lib.redis_client.RedisClient', autospec=True)
    @mock.patch('threading.Thread', autospec=True)
    def setUpNoThread(self, mock_thread, mock_redis):
        self.setUpQueues()
        self.deduplicator = deduplicator.Deduplicator(
            in_q=self.in_q,
            out_q=self.out_q)

    @mock.patch('lib.redis_client.RedisClient', autospec=True)
    def setUpWithThread(self, mock_redis):
        self.setUpQueues()
        self.deduplicator = deduplicator.Deduplicator(
            in_q=self.in_q,
            out_q=self.out_q)

    def setUpQueues(self):
        self.in_q = queue.Queue()
        self.out_q = queue.Queue()

    def test_run(self):
        self.setUpNoThread()
        self.deduplicator.run()
        self.deduplicator.worker_thread.start.assert_called_once_with()

    def test_shutdown(self):
        self.setUpWithThread()
        self.deduplicator.run()
        self.assertEqual(self.deduplicator.worker_thread.is_alive(), True)
        self.deduplicator.shutdown()
        self.assertEqual(self.deduplicator.worker_thread.is_alive(), False)

    def test_process_q_not_duplicate(self):
        self.setUpWithThread()
        testobject = TestClass()
        testvalue = pickle.dumps(testobject)

        self.deduplicator.redis.is_duplicate.return_value = False
        self.deduplicator.run()
        self.in_q.put(testvalue)
        self.assertEqual(self.out_q.get(), testvalue)
        self.deduplicator.shutdown()

    def test_process_q_duplicate(self):
        self.setUpWithThread()
        testobject = TestClass()
        testvalue = pickle.dumps(testobject)

        self.in_q.put(testvalue)
        self.deduplicator.redis.is_duplicate.return_value = True
        self.deduplicator.run()
        self.assertRaises(queue.Empty, self.out_q.get, block=False)
        self.deduplicator.shutdown()
