import abc
import threading
import pickle


class QueueFilterBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def process_q_msg(self):
        pass

    def __init__(self, *args, **kwargs):
        self._shutdown = False
        self.in_q = kwargs['in_q']
        self.out_q = kwargs['out_q']
        self.worker_thread = threading.Thread(
            name='worker_thread',
            target=self.process_q)

    def run(self):
        self.worker_thread.start()

    def process_q(self):
        while True:
            msg = self.in_q.get(block=True)
            if self._shutdown:
                break
            result = self.process_q_msg(pickle.loads(msg))
            if result:
                self.out_q.put(pickle.dumps(result))

    def shutdown(self):
        self._shutdown = True
        # make the processing loop cycle one last time
        self.in_q.put('shutdown')
        self.worker_thread.join()
