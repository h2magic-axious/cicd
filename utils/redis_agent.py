import redis

from utils.environments import Env


class _RedisSession:
    def __init__(self):
        self.client = redis.Redis(connection_pool=redis.ConnectionPool(
            host=Env.REDIS_HOST,
            port=Env.REDIS_PORT,
            password=Env.REDIS_PASSWORD,
            decode_responses=True,
            db=Env.REDIS_SELECT,
            max_connections=100
        ))


RedisSession = _RedisSession()
