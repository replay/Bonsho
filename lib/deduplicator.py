from lib import redis_client
from lib import queue_filter_base


class Deduplicator(queue_filter_base.QueueFilterBase):

    def __init__(self, *args, **kwargs):
        super(Deduplicator, self).__init__(*args, **kwargs)
        self.redis = redis_client.RedisClient()

    def process_q_msg(self, transaction):
        if not self.redis.is_duplicate(transaction.hash):
            return transaction
