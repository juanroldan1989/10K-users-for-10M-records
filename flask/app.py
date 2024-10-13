from flask import Flask, render_template, request, jsonify
from db import get_db_connection, release_db_connection, close_connection_pool, initialize_pool
import os

app = Flask(__name__)

# Initialize the connection pool
initialize_pool() if os.environ.get('USE_POOLING') == 'true' else None

@app.route('/')
def index():
  conn = get_db_connection()
  if conn is None:
    return "Error connecting to the database", 500

  cur = conn.cursor()
  # Fetch 10 distinct locations from the database
  cur.execute("SELECT DISTINCT location FROM weather_data LIMIT 10")
  locations = [row[0] for row in cur.fetchall()]
  cur.close()
  release_db_connection(conn)

  # Pass locations to the template
  return render_template('index.html', locations=locations)

@app.route('/query', methods=['POST'])
def query():
  location = request.form.get('location')
  if location is None or location == '':
    return "No location specified", 500

  conn = get_db_connection()
  if conn is None:
    return "Error connecting to the database", 500

  print(f"Fetching data for location: {location}")

  cur = conn.cursor()
  cur.execute("SELECT AVG(temperature) FROM weather_data WHERE location = %s", (location,))
  average_temperature = cur.fetchone()[0]
  cur.close()
  release_db_connection(conn)

  average_temperature = f"{average_temperature:.2f} °C" if average_temperature is not None else "No data available"

  return render_template('results.html', location=location, avg_temp=average_temperature)

@app.route('/health', methods=['GET'])
def health():
  return jsonify(status='ok', message='Healthy', code=200)
