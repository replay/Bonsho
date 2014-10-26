import threading


class Deduplicator:

    def __init__(self, **kwargs):
        self.in_q = kwargs['in_q']
        self.out_q = kwargs['out_q']
        self.worker_thread = threading.Thread(
            name='deduplicator',
            target=self.process_q)

    def process(self):
        self.worker_thread.start()

    def process_q(self):
        while True:
            item = self.in_q.get(block=True)
            print("got item: {0}".format(item))
