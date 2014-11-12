from lib import queue_filter_base


class WebsocketsApi(queue_filter_base.QueueFilterBase):

    def __init__(self, *args, **kwargs):
        super(WebsocketsApi, self).__init__(*args, **kwargs)

    def process_q_msg(self, transaction):
        print(transaction)
