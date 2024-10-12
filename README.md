# 10K-users-for-10M-records

# 10M records

To populate a PostgreSQL database with 10 million time series records:

- Random weather forecast data is generated and
- Inserted it into PostgreSQL database.
- For large data insertions, `psycopg2` library performs batch inserts for better performance.

Script to generate synthetic weather data (e.g., temperature, humidity, wind speed) with timestamps for each entry:

```ruby
def generate_weather_data():
  location = fake.city()
  temperature = round(random.uniform(-10, 40), 2)  # Temperature in Celsius
  humidity = round(random.uniform(20, 100), 2)     # Humidity in percentage
  wind_speed = round(random.uniform(0, 20), 2)     # Wind speed in m/s
  timestamp = fake.date_time_between(start_date="-5y", end_date="now")
  return (location, temperature, humidity, wind_speed, timestamp)

# Insert data into the database in batches for better performance
batch_size = int(os.environ.get('BATCH_SIZE', 1000))
total_records = int(os.environ.get('TOTAL_RECORDS', 10000)) # 10 million records
records_inserted = 0

while records_inserted < total_records:
  batch = [generate_weather_data() for _ in range(batch_size)]
  args_str = ",".join(cur.mogrify("(%s, %s, %s, %s, %s)", record).decode("utf-8") for record in batch)
  cur.execute(f"INSERT INTO weather_data (location, temperature, humidity, wind_speed, timestamp) VALUES {args_str}")
  conn.commit()
  records_inserted += batch_size
  print(f"{records_inserted}/{total_records} records inserted")
```

- **Faker:** Generates random locations and timestamps.
- **Random:** Generates random temperature, humidity, and wind speed values.
- **Batch Insertion:** Inserting data in batches of **10,000 records** for better performance (`BATCH_SIZE` & `TOTAL_RECORDS`)

## Docker Compose

3 services are launched: **db**, **data-populator** and **data-query**

1. **db** contains a PostgreSQL database
2. **data-populator** inserts data in **db** once **db**'s condition is **service_healthy**
3. **data-query** performs queries in **db** once **data-populator**'s condition is **service_completed_successfully**
4. **flask** application to query **temperature** data by **location**

```ruby
$ docker-compose up
...

db              |
db              | PostgreSQL Database directory appears to contain a database; Skipping initialization
db              |
db              | 2024-10-12 09:29:24.491 UTC [1] LOG:  starting PostgreSQL 13.16 (Debian 13.16-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
db              | 2024-10-12 09:29:24.491 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db              | 2024-10-12 09:29:24.491 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db              | 2024-10-12 09:29:24.497 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db              | 2024-10-12 09:29:24.506 UTC [27] LOG:  database system was shut down at 2024-10-12 09:25:03 UTC
db              | 2024-10-12 09:29:24.516 UTC [1] LOG:  database system is ready to accept connections

data-populator  | 1000/10000 records inserted
data-populator  | 2000/10000 records inserted
data-populator  | 3000/10000 records inserted
data-populator  | 4000/10000 records inserted
data-populator  | 5000/10000 records inserted
data-populator  | 6000/10000 records inserted
data-populator  | 7000/10000 records inserted
data-populator  | 8000/10000 records inserted
data-populator  | 9000/10000 records inserted
data-populator  | 10000/10000 records inserted
data-populator  | Database connection closed
data-populator exited with code 0

data-query      | 5 distinct locations in the database:
data-query      | Port Tiffanyhaven
data-query      | North Amandaport
data-query      | Gabrielside
data-query      | South Philipfort
data-query      | Port Margaretland
data-query      |
data-query      | Fetching data for location: Port Tiffanyhaven
data-query      | Average temperature in Port Tiffanyhaven: 2.44°C
data-query      |
data-query      | Fetching data for location: North Amandaport
data-query      | Average temperature in North Amandaport: 23.71°C
data-query      |
data-query      | Fetching data for location: Gabrielside
data-query      | Average temperature in Gabrielside: 29.71°C
data-query      |
data-query      | Fetching data for location: South Philipfort
data-query      | Average temperature in South Philipfort: 36.44°C
data-query      |
data-query      | Fetching data for location: Port Margaretland
data-query      | Average temperature in Port Margaretland: 8.81°C
data-query      | Database connection closed
data-query exited with code 0
```
