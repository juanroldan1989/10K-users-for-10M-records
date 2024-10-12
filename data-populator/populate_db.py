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

# Connect to PostgreSQL database
conn = psycopg2.connect(
  host=POSTGRES_HOST,
  database=POSTGRES_DB,
  user=POSTGRES_USER,
  password=POSTGRES_PASSWORD
)

cur = conn.cursor()

# Create table if not exists
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
