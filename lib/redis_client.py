import redis
import time


class RedisClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.conn_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.redis = redis.Redis(connection_pool=self.conn_pool)

    def _get_time(self):
        return int(time.time())

    def is_duplicate(self, hash_string):
        old_value = self.redis.getset(hash_string, self._get_time())
        if not old_value:
            return False
        return old_value
