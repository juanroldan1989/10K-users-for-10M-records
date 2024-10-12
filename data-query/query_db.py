# Query the Database -> Fetch the average temperature for a specific location

import os
import psycopg2

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

# Fetch 5 distinct locations from the database
cur.execute("SELECT DISTINCT location FROM weather_data LIMIT 5")
locations = cur.fetchall()
print("5 distinct locations in the database:")
for location in locations:
    print(location[0])

# Iterate over each location and fetch the filtered results
for location_tuple in locations:
    location = location_tuple[0]  # Extract the location from the tuple
    print(f"\nFetching data for location: {location}")

    cur.execute("SELECT AVG(temperature) FROM weather_data WHERE location = %s", (location,))
    average_temperature = cur.fetchone()[0]

    if average_temperature is not None:
        print(f"Average temperature in {location}: {average_temperature:.2f}°C")
    else:
        print(f"No data available for {location}")

# Close the connection
cur.close()
conn.close()
print("Database connection closed")
