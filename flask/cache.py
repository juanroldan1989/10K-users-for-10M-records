import redis
import os
import json

from flask import jsonify
from redis_client import get_redis_client

# Check if caching is enabled
caching_enabled = os.environ.get('CACHE', 'false').lower() == 'true'
cache_expiry = int(os.environ.get('CACHE_EXPIRY', 300))

def cache_query(key, fetch_function):
  redis_client = get_redis_client()  # Use the memoized Redis client

  if not caching_enabled:
    return fetch_function()  # Fetch without caching

  try:
    if redis_client.exists(key):
      print(f"Cache hit for key: {key}")
      # Return cached data
      return json.loads(redis_client.get(key))

    print(f"Cache miss for key: {key}")
    # Fetch fresh data and cache it
    data = fetch_function()
    redis_client.set(key, json.dumps(data), ex=300)  # Cache for 5 minutes
    return data

  except redis.exceptions.RedisError as e:
    # If Redis is down or there's an issue, fall back to fetching fresh data
    print(f"Redis error for key: {key} - {e}")
    return fetch_function()
