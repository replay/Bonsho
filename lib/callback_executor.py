import requests
import pickle
from lib import queue_filter_base
from lib import config


class CallbackExecutor(queue_filter_base.QueueFilterBase):

    def __init__(self, *args, **kwargs):
        super(CallbackExecutor, self).__init__(*args, **kwargs)
        self.config = config.Configuration()['Callback']

    def process_q_msg(self, transaction):
        import pdb
        pdb.set_trace()
        requests.post(self.config['endpoint'], data=pickle.dumps(transaction))
