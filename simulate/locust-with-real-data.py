from locust import HttpUser, TaskSet, task
import random
import os
import psycopg2

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

class UserBehavior(TaskSet):
  @task
  def query_weather(self):
    conn = get_db_connection()
    if conn:
      try:
        cur = conn.cursor()
        # Fetch 10 distinct locations from the database
        cur.execute("SELECT DISTINCT location FROM weather_data LIMIT 10")
        locations = cur.fetchall()
        cur.close()

        location_names = [location[0] for location in locations]
        print(f"10 distinct locations in the database: {location_names}")

        if location_names:
          # Query the database for a random location
          selected_location = random.choice(location_names)
          self.client.post("/query", data={'location': random.choice(selected_location)})
        else:
          print("No locations available in the database")

      except psycopg2.Error as e:
        print(f"Error querying the database: {e}")
      finally:
        conn.close()
        print("Database connection closed")

class WebsiteUser(HttpUser):
  tasks = [UserBehavior]
  min_wait = 1000  # wait between tasks in milliseconds
  max_wait = 2000
