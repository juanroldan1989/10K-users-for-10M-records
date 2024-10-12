# Populate PostgreSQL database with random weather data

import os
import psycopg2
import random
import datetime
from faker import Faker

# Setup Faker for random data generation
fake = Faker()

# Get database connection details from environment variables
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

# Database connection
def get_db_connection():
  try:
    conn = psycopg2.connect(
      host=os.environ.get('POSTGRES_HOST', 'localhost'),
      database=os.environ.get('POSTGRES_DB', 'mydb'),
      user=os.environ.get('POSTGRES_USER', 'user'),
      password=os.environ.get('POSTGRES_PASSWORD', 'password')
    )
    return conn
  except psycopg2.OperationalError as e:
    print(f"Error connecting to the database: {e}")
    return None

conn = get_db_connection()
cur = conn.cursor()

print("Creating 'weather_data' table if not exists...")
cur.execute('''
CREATE TABLE IF NOT EXISTS weather_data (
  id SERIAL PRIMARY KEY,
  location VARCHAR(100),
  temperature FLOAT,
  humidity FLOAT,
  wind_speed FLOAT,
  timestamp TIMESTAMPTZ
);
''')
conn.commit()
print("'weather_data' table created successfully")

print("Creating index on 'location' column...")
cur.execute('''
CREATE INDEX IF NOT EXISTS location_idx ON weather_data (location);
''')
conn.commit()
print("Index created successfully")

# Function to generate random weather data
def generate_weather_data():
  location = fake.city()
  temperature = round(random.uniform(-10, 40), 2)  # Temperature in Celsius
  humidity = round(random.uniform(20, 100), 2)     # Humidity in percentage
  wind_speed = round(random.uniform(0, 20), 2)     # Wind speed in m/s
  timestamp = fake.date_time_between(start_date="-5y", end_date="now")
  return (location, temperature, humidity, wind_speed, timestamp)

# Insert data into the database in batches for better performance
batch_size = int(os.environ.get('BATCH_SIZE', 1000))
total_records = int(os.environ.get('TOTAL_RECORDS', 10000))

# Check the current number of records in the database
cur.execute("SELECT COUNT(*) FROM weather_data;")
current_records = cur.fetchone()[0]

# Calculate how many more records need to be inserted
records_needed = total_records - current_records
if records_needed <= 0:
  print("The database already contains the required number of records.")
else:
  print(f"Adding {records_needed} records to the database...")
  records_inserted = 0

  while records_inserted < total_records:
    batch = [generate_weather_data() for _ in range(batch_size)]
    args_str = ",".join(cur.mogrify("(%s, %s, %s, %s, %s)", record).decode("utf-8") for record in batch)
    cur.execute(f"INSERT INTO weather_data (location, temperature, humidity, wind_speed, timestamp) VALUES {args_str}")
    conn.commit()
    records_inserted += batch_size
    print(f"{records_inserted}/{total_records} records inserted")

  # Close the connection
  cur.close()
  conn.close()
  print("Database connection closed")
