import threading
import pickle
from lib import redis_client


class Deduplicator:

    def __init__(self, **kwargs):
        self._shutdown = False
        self.in_q = kwargs['in_q']
        self.out_q = kwargs['out_q']
        self.redis = redis_client.RedisClient()
        self.worker_thread = threading.Thread(
            name='deduplicator',
            target=self.process_q)

    def process(self):
        self.worker_thread.start()

    def process_q(self):
        while not self._shutdown:
            transaction = pickle.loads(self.in_q.get(block=True))
            if not self.redis.is_duplicate(transaction.hash):
                print(pickle.dumps(transaction))
                self.out_q.put(pickle.dumps(transaction))

    def shutdown(self):
        self._shutdown = True
        # make the processing loop cycle one last time
        self.in_q.put('shutdown')
        self.worker_thread.join()
