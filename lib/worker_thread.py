import abc
import threading


class WorkerThread(metaclass=abc.ABCMeta):

    def __init__(self, *args, **kwargs):
        self.worker_thread = threading.Thread(
            name='worker_thread',
            target=self.worker_method)

    def run(self):
        self.worker_thread.start()
