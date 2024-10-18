from flask import Flask, render_template, request, jsonify
from flask_caching import Cache
from db import initialize_pool
from db_queries import get_locations, get_average_temperature
from cache import cache_query

import os

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = os.environ.get('REDIS_HOST')
app.config['CACHE_REDIS_PORT'] = os.environ.get('REDIS_PORT')

# Initialize the connection pool
initialize_pool() if os.environ.get('USE_POOLING') == 'true' else None
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/')
@cache.cached(timeout=300) # Cache the query for 5 minutes
def index():
  locations = cache_query('locations', get_locations)
  return render_template('index.html', locations=locations)

@cache.cached(timeout=300, query_string=True) # Cache query results based on request parameters for 5 minutes
@app.route('/query', methods=['POST'])
def query():
  location = request.form.get('location')
  if location is None or location == '':
    return "No location specified", 500

  average_temperature = cache_query(location, lambda: get_average_temperature(location))
  average_temperature = f"{average_temperature:.2f} °C" if average_temperature is not None else "No data available"

  return render_template('results.html', location=location, avg_temp=average_temperature)

@app.route('/health-check')
def health_check():
  return "success"
