from flask import Flask, render_template, request, jsonify
from db import initialize_pool
from db_queries import get_locations, get_average_temperature
from cache import cache_query

import os

app = Flask(__name__)

# Initialize the connection pool
initialize_pool() if os.environ.get('USE_POOLING') == 'true' else None

@app.route('/')
def index():
  locations = cache_query('locations', get_locations)
  return render_template('index.html', locations=locations)

@app.route('/query', methods=['POST'])
def query():
  location = request.form.get('location')
  if location is None or location == '':
    return "No location specified", 500

  average_temperature = cache_query(location, lambda: get_average_temperature(location))
  average_temperature = f"{average_temperature:.2f} °C" if average_temperature is not None else "No data available"

  return render_template('results.html', location=location, avg_temp=average_temperature)

@app.route('/health', methods=['GET'])
def health():
  return jsonify(status='ok', message='Healthy', code=200)
