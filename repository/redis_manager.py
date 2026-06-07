from config.config import Config
import redis

config = Config()
redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
