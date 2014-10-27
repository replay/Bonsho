import threading


class Deduplicator:

    def __init__(self, **kwargs):
        self._shutdown = False
        self.in_q = kwargs['in_q']
        self.out_q = kwargs['out_q']
        self.worker_thread = threading.Thread(
            name='deduplicator',
            target=self.process_q)

    def process(self):
        self.worker_thread.start()

    def process_q(self):
        while not self._shutdown:
            self.in_q.get(block=True)

    def shutdown(self):
        self._shutdown = True
        self.in_q.put('trigger process loop')
        self.worker_thread.join()
