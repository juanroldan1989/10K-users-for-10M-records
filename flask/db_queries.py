from db import get_db_connection, release_db_connection

def get_locations():
  conn = get_db_connection()
  if conn is None:
    return "Error connecting to the database", 500

  print("Fetching 10 distinct locations from the database")

  cur = conn.cursor()
  cur.execute("SELECT DISTINCT location FROM weather_data LIMIT 10")
  locations = [row[0] for row in cur.fetchall()]
  cur.close()
  release_db_connection(conn)
  return locations

def get_average_temperature(location):
  conn = get_db_connection()
  if conn is None:
    return "Error connecting to the database", 500

  print(f"Fetching average temperature for location: {location}")

  cur = conn.cursor()
  cur.execute("SELECT AVG(temperature) FROM weather_data WHERE location = %s", (location,))
  average_temperature = cur.fetchone()[0]
  cur.close()
  release_db_connection(conn)

  return average_temperature
