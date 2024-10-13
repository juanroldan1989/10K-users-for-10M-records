import redis
import os
import json
from flask import jsonify

# Initialize Redis client
redis_host = os.environ.get('REDIS_HOST')
redis_port = int(os.environ.get('REDIS_PORT'))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Check if caching is enabled
caching_enabled = os.environ.get('CACHE', 'false').lower() == 'true'
cache_expiry = int(os.environ.get('CACHE_EXPIRY', 300))

def cache_query(key, fetch_function):
  if not caching_enabled:
    return fetch_function()  # Fetch without caching

  if redis_client.exists(key):
    print(f"Cache hit for key: {key}")
    # Return cached data
    return json.loads(redis_client.get(key))

  print(f"Cache miss for key: {key}")
  # Fetch fresh data and cache it
  data = fetch_function()
  redis_client.set(key, json.dumps(data), ex=300)  # Cache for 5 minutes
  return data
