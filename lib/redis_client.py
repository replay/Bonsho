import redis
import time
from lib import config as project_config


class RedisClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        config = project_config.Configuration()['Redis']
        self.conn_pool = redis.ConnectionPool(
            host=config['host'],
            port=int(config['port']),
            db=int(config['db']))
        self.redis = redis.Redis(connection_pool=self.conn_pool)

    def _get_time(self):
        return int(time.time())

    def is_duplicate(self, hash_string):
        return self.redis.getset(hash_string, self._get_time())
