from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
  conn = psycopg2.connect(
    host=os.environ.get('POSTGRES_HOST', 'localhost'),
    database=os.environ.get('POSTGRES_DB', 'mydb'),
    user=os.environ.get('POSTGRES_USER', 'user'),
    password=os.environ.get('POSTGRES_PASSWORD', 'password')
  )
  return conn

@app.route('/')
def index():
  conn = get_db_connection()
  cur = conn.cursor()

  # Fetch 10 distinct locations from the database
  cur.execute("SELECT DISTINCT location FROM weather_data LIMIT 10")
  locations = [row[0] for row in cur.fetchall()]

  cur.close()
  conn.close()

  # Pass locations to the template
  return render_template('index.html', locations=locations)

@app.route('/query', methods=['POST'])
def query():
  location = request.form.get('location')
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("SELECT AVG(temperature) FROM weather_data WHERE location = %s", (location,))
  average_temperature = cur.fetchone()[0]
  cur.close()
  conn.close()

  return render_template('results.html', location=location, avg_temp=f"{average_temperature:.2f}")
