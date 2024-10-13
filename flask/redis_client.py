import redis
import os

redis_client = None  # Global variable to hold the Redis client

def get_redis_client():
  global redis_client

  if redis_client is None:
    redis_host = os.environ.get('REDIS_HOST')
    redis_port = int(os.environ.get('REDIS_PORT'))
    redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

  return redis_client
