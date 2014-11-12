import abc
import threading
import pickle
from lib import worker_thread


class QueueFilterBase(worker_thread.WorkerThread, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def process_q_msg(self):
        pass

    def __init__(self, *args, **kwargs):
        self._shutdown = False
        self.in_q = kwargs['in_q']
        if 'out_q' in kwargs:
            self.out_q = kwargs['out_q']
        self.worker_method = self.process_q
        super(QueueFilterBase, self).__init__(*args, **kwargs)

    def process_q(self):
        while True:
            msg = self.in_q.get(block=True)
            if self._shutdown:
                break
            result = self.process_q_msg(pickle.loads(msg))
            if result and hasattr(self, 'out_q'):
                self.out_q.put(pickle.dumps(result))

    def shutdown(self):
        self._shutdown = True
        # make the processing loop cycle one last time
        self.in_q.put('shutdown')
        self.worker_thread.join()
