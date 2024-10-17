![Screenshot 2024-10-12 at 16 43 48](https://github.com/user-attachments/assets/dcf8329d-2e59-452b-9626-49b6032dfb41)

<h4 align="center">10M records | 10K users | Query by script & UI | Docker Compose | Terraform </h4>

<p align="center">
  <a href="https://github.com/juanroldan1989/10K-users-for-10M-records/commits/main">
  <img src="https://img.shields.io/github/last-commit/juanroldan1989/10K-users-for-10M-records.svg?style=flat-square&logo=github&logoColor=white" alt="GitHub last commit">
  <a href="https://github.com/juanroldan1989/10K-users-for-10M-records/issues">
  <img src="https://img.shields.io/github/issues-raw/juanroldan1989/10K-users-for-10M-records.svg?style=flat-square&logo=github&logoColor=white" alt="GitHub issues">
  <a href="https://github.com/juanroldan1989/10K-users-for-10M-records/pulls">
  <img src="https://img.shields.io/github/issues-pr-raw/juanroldan1989/10K-users-for-10M-records.svg?style=flat-square&logo=github&logoColor=white" alt="GitHub pull requests">
  <a href="https://github.com/juanroldan1989/10K-users-for-10M-records/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-brightgreen.svg">
  </a>
</p>

<p align="center">
  <a href="#10k-records">10M Records</a> •
  <a href="#docker-compose">Docker Compose</a> •
  <a href="#development">Development</a>  •
  <a href="#contribute">Contribute</a>
</p>

# 10M records

https://github.com/juanroldan1989/10K-users-for-10M-records/blob/main/data-populator/populate_db.py

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
- **Batch Insertion:** Inserting data in batches of **10,000 records** for better performance
- Populate **parameters**: `BATCH_SIZE` & `TOTAL_RECORDS`

# 10K Users

https://github.com/juanroldan1989/10K-users-for-10M-records/tree/main/simulate

1. Tools like `Locust` or `Apache JMeter` can be used to simulate concurrent users interacting with a Flask application.

```ruby
pip install locust
```

2. Write a Locustfile: Create a file named locustfile.py with the following content:

```ruby
from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):
  @task
  def query_weather(self):
    locations = ['Aaronfort', 'Abigailton', 'Abigailtown', 'Acevedofourt', 'Abigailshire']
    # GET homepage
    self.client.get('/')
    # POST query to server
    # self.client.post('/query', data={'location': random.choice(locations)})

class WebsiteUser(HttpUser):
  tasks = [UserBehavior]
  min_wait = 1000 # wait between tasks in milliseconds
  max_wait = 2000
```

- Run Locust to reach app home page:

```ruby
locust -f get-request-home-page.py --host=http://localhost:8000
```

- Run Locust using a static list of 10 locations harcoded:

```ruby
locust -f post-request-api-and-db.py --host=http://localhost:8000
```

3. Access `http://localhost:8089` in browser to start the test, where you can configure the number of users to simulate.

4. Run your Flask application locally to ensure the UI works as expected. Run Locust to simulate 1K concurrent users and monitor the performance.

https://github.com/juanroldan1989/10K-users-for-10M-records/tree/main/flask

# The App

1. User chooses Location from dropdown.
2. User submits form.
3. App queries database.
4. Average Temperature for Location is displayed.

https://github.com/user-attachments/assets/1d0b4d84-8a58-40ff-b60d-950a78242331

# Locust

Access `http://localhost:8089` in browser to start the test, where you can configure all the parameters:

![Screenshot 2024-10-12 at 16 59 48](https://github.com/user-attachments/assets/7ba96957-6241-40e3-abd6-399e88fb28c9)

1. **Number of users (peak concurrency)**: This field defines how many users (or virtual users, VUs) you want Locust to simulate concurrently during the load test.

- These users represent the number of clients that are sending requests to your system at the same time.

- Example: If you set "Number of users" to 1000, Locust will simulate 1000 users simultaneously sending requests to the target system. This simulates how your system would handle a real-world load of 1000 concurrent users.

2. **Ramp up (users started/second)**: This field controls how fast Locust will start new users during the test. It specifies the number of users that will be started per second.

- Example: If you set "Ramp up" to **10**, Locust will add **10 new users per second** until it reaches the total number specified in the "Number of users" field.

- This feature allows you to gradually increase the load instead of starting all users at once, which simulates a more realistic load scenario where users gradually connect to the system over time.

3. **Example Scenario:**

- Number of users (peak concurrency): **1000**
- Ramp up (users started/second): **50**

In this case, Locust will:

- Start **50 users** per second.
- After 20 seconds, Locust will have reached **1000 users** (50 users \* 20 seconds = 1000 users).
- Once the 1000 users are reached, the **test will continue with those 1000 users until you stop it** or the test reaches a defined time limit.

# Local - Load Testing scenarios

- Number of users (peak concurrency): **1000**
- Ramp up (users started/second): **10**

## Random `location` submitted from each user

```ruby
API - POST `/query` -> `(data: { location: "<random-location-value>" })`
```

https://github.com/juanroldan1989/10K-users-for-10M-records/blob/main/simulate/post/random-locations.py

![total_requests_per_second_random_locations](https://github.com/user-attachments/assets/d8b3d81c-5a8d-47d4-985e-2165edfec6ba)

- Flask API Returns `AVG Temperature` for `location`
- **1** Postgres DB instance
- **1** NGINX container (load-balancing configured) serving requests to `Flask` containers

```ruby
...
upstream flask {
  server flask:5000;
  server flask_replica_1:5000;
  server flask_replica_2:5000;
}
...
```

- **3** FLASK containers
- Each **Flask** container with caching **enabled**
- **Database Connection Pooling** logic enabled:

https://github.com/juanroldan1989/10K-users-for-10M-records/blob/main/flask/db.py

```ruby
def get_db_connection():
  if USE_POOLING and connection_pool:
    try:
      conn = connection_pool.getconn()
      if conn:
        return conn
    except Exception as e:
      print(f"Error getting connection from pool: {e}")
  else:
    try:
      conn = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'),
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
      )
      return conn
    except psycopg2.OperationalError as e:
      print(f"Error connecting to the database: {e}")
      return None
```

- Each **Flask** container with connection pooling **enabled**:

```ruby
...
USE_POOLING: "true"
POOL_MINCONN: 5
POOL_MAXCONN: 15
...
```

## Fixed `location` submitted from each user

```ruby
API - POST `/query` -> `(data: { location: "<fixed-location-value>" })`
```

https://github.com/juanroldan1989/10K-users-for-10M-records/blob/main/simulate/post/fixed-location.py

- In a real-world scenario, users might query the same location repeatedly, e.g., a user checking **weather for their hometown**
- We **assign each virtual user** a specific location and have them **always query the same** one throughout their session.

![total_requests_per_second_fixed_locations](https://github.com/user-attachments/assets/8991c0ac-e0d0-463d-bb69-2f663bffefe6)

Components:

- Flask API Returns `AVG Temperature` for `location`
- **1** Postgres DB instance
- **1** NGINX container (load-balancing configured) serving requests to `Flask` containers
- **3** FLASK containers
- Each **Flask** container with connection pooling **enabled**
- Each **Flask** container with caching **enabled**

## Weighted `location` submitted from each user

```ruby
API - POST `/query` -> `(data: { location: "<weigthed-location-value>" })`
```

https://github.com/juanroldan1989/10K-users-for-10M-records/blob/main/simulate/post/weighted-locations.py

- Showcasing **hot spots** for location values
- where **certain** locations are queried **more frequently** than others
- increasing the **likelihood** of cache hits.

![total_requests_per_second_weighted_locations](https://github.com/user-attachments/assets/14a7bbd0-4924-4639-8791-8c3a4cd9431c)

Components:

- Flask API Returns `AVG Temperature` for `location`
- **1** Postgres DB instance
- **1** NGINX container (load-balancing configured) serving requests to `Flask` containers
- **3** FLASK containers
- Each **Flask** container with connection pooling **enabled**
- Each **Flask** container with caching **enabled**

## Conclusions

- Performing a load test within an application is not only about **load-balancing**, **caching** or **database connection pooling mechanisms**.

- It's also important to define **proper experiments**

- This way, results provide **valuable insights** and engineers can improve platforms accordingly.

- Both **fixed location** and **weighted location** experiments showed `Response Time` remained under `~6s` with `~800 users per second` was reached.

- **weighted location** experiment showed `Response Time` remained under `~6s` all the way until `~1000 users per second` was reached.

- **random location** experiment showed `Response Time` slower than other 2 experiments. From this I can gather:

1. **The way response times are measured can also influence the perceived performance.**

- For example, if the first request for a "random location" is a cache miss and takes longer, while subsequent requests benefit from caching, **this can skew the average response time.**

2. **The nature of the data might lead to varied response times.**

- For instance, if most of your database records pertain to a few popular locations, those queries will naturally be faster.

# AWS - Load Testing scenarios

[work in progress]

- Number of users (peak concurrency): **1000**
- Ramp up (users started/second): **10**

## Provision Infrastructure

### Docker Images (build/push)

#### Option 1: Build/Push all required images with 1 script

```ruby
$ ./build_and_push_images.sh
```

#### Option 2: Buid/Push images separately (ideal when making adjustments to specific images)

1. Build `data-populator` image and push to Docker Hub.

```ruby
$ cd data-populator

$ docker build -t juanroldan1989/data-populator .
$ docker push juanroldan1989/data-populator:latest
```

2. Build `data-query` image and push to Docker Hub.

```ruby
$ cd data-query

$ docker build -t juanroldan1989/data-query .
$ docker push juanroldan1989/data-query:latest
```

3. Build `flask` image and push to Docker Hub.

```ruby
$ cd flask

$ docker build -t juanroldan1989/flask .
$ docker push juanroldan1989/flask:latest
```

4. Build `nginx` image and push to Docker Hub.

```ruby
$ cd nginx

$ docker build -t juanroldan1989/nginx .
$ docker push juanroldan1989/nginx:latest
```

### Terraform

1. Change dir to a project `ecs-fargate-nginx-flask-db`
2. Run commands:

```ruby
$ terraform init
$ terraform apply
```

3. Check `output` section

```ruby
alb_dns_name = "ecs-alb-<account-id>.<region-id>.elb.amazonaws.com"
```

4. Available endpoints are:

## Random `location` submitted from each user

```ruby
API - POST `/query` -> `(data: { location: "<random-location-value>" })`
```

...

# Development

https://github.com/juanroldan1989/10K-users-for-10M-records/blob/main/docker-compose.yaml

```ruby
$ docker-compose up
```

## Containers

6 containers are started: **db**, **redis**, **data-populator**, **data-query**, **flask** and **nginx**.

1. **db** contains a PostgreSQL database

2. **redis** containers a Redis instance

3. **data-populator** inserts data in **db** once **db**'s condition is **service_healthy**
   https://github.com/juanroldan1989/10K-users-for-10M-records/tree/main/data-populator

4. **data-query** performs **health-check** queries in **db** once **data-populator**'s condition is **service_completed_successfully**
   https://github.com/juanroldan1989/10K-users-for-10M-records/tree/main/data-query

5. **flask** application with UI to query **temperature** data by **location**
   https://github.com/juanroldan1989/10K-users-for-10M-records/tree/main/flask

6. **NGINX** reverse-proxy and load-balancer instance added. `nginx/default.conf` and `nginx/default.conf.alternative` files added with **reverse-proxy only** and **reverse-proxy + load-balancer** configurations respectively.
   https://github.com/juanroldan1989/10K-users-for-10M-records/tree/main/nginx

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

redis            | 1:C 13 Oct 2024 15:42:40.248 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis            | 1:C 13 Oct 2024 15:42:40.249 * Redis version=7.4.1, bits=64, commit=00000000, modified=0, pid=1, just started
redis            | 1:C 13 Oct 2024 15:42:40.249 * Configuration loaded
redis            | 1:M 13 Oct 2024 15:42:40.250 * monotonic clock: POSIX clock_gettime
redis            | 1:M 13 Oct 2024 15:42:40.251 * Running mode=standalone, port=6379.
redis            | 1:M 13 Oct 2024 15:42:40.252 * Server initialized
redis            | 1:M 13 Oct 2024 15:42:40.252 * Loading RDB produced by version 7.4.1
redis            | 1:M 13 Oct 2024 15:42:40.252 * RDB age 890 seconds
redis            | 1:M 13 Oct 2024 15:42:40.252 * RDB memory usage when created 1.02 Mb
redis            | 1:M 13 Oct 2024 15:42:40.252 * Done loading RDB, keys loaded: 0, keys expired: 5.
redis            | 1:M 13 Oct 2024 15:42:40.252 * DB loaded from disk: 0.000 seconds
redis            | 1:M 13 Oct 2024 15:42:40.252 * Ready to accept connections tcp

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

flask           | [2024-10-12 13:06:24 +0000] [1] [INFO] Starting gunicorn 23.0.0
flask           | [2024-10-12 13:06:24 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
flask           | [2024-10-12 13:06:24 +0000] [1] [INFO] Using worker: sync
flask           | [2024-10-12 13:06:24 +0000] [6] [INFO] Booting worker with pid: 6
flask           | [2024-10-12 13:06:24 +0000] [7] [INFO] Booting worker with pid: 7
flask           | [2024-10-12 13:06:24 +0000] [8] [INFO] Booting worker with pid: 8

nginx            | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx            | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx            | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx            | 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
nginx            | 10-listen-on-ipv6-by-default.sh: info: /etc/nginx/conf.d/default.conf differs from the packaged version
nginx            | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx            | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx            | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx            | /docker-entrypoint.sh: Configuration complete; ready for start up
```

Access: `http://localhost:5000`

1. Choose Location from dropdown
2. Check Average Temperature on Location
3. Adjust source code as needed within `flask` folder.
4. Run `docker-compose up --build`

# Bottlenecks & Fixes

## Too many database queries

- Caching **locations** results to avoid querying the database repeatedly for **the same data**.

- This cache could be **refreshed** periodically (e.g., every few minutes) while the script runs.

```ruby
# cache.py

import redis
import os
import json
from flask import jsonify

# Initialize Redis client
redis_host = os.environ.get('REDIS_HOST')
redis_port = int(os.environ.get('REDIS_PORT'))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Check if caching is enabled
caching_enabled = os.environ.get('CACHE', 'false').lower() == 'true'
cache_expiry = int(os.environ.get('CACHE_EXPIRY', 300))

def cache_query(key, fetch_function):
  if not caching_enabled:
    return fetch_function()  # Fetch without caching

  if redis_client.exists(key):
    print(f"Cache hit for key: {key}")
    # Return cached data
    return json.loads(redis_client.get(key))

  print(f"Cache miss for key: {key}")
  # Fetch fresh data and cache it
  data = fetch_function()
  redis_client.set(key, json.dumps(data), ex=300)  # Cache for 5 minutes
  return data
```

### Benefits

- Avoids constant database reads, as locations are cached in redis.
- Reduces load on the database by limiting the frequency of queries.

## Sorry, too many clients already

From `docker-compose` logs:

```ruby
...
db | 2024-10-12 14:35:35.208 UTC [4499] FATAL:  sorry, too many clients already
...
```

### Connection Pooling

- Instead of opening and closing a new database connection with every request, we can use a connection pool.

- Connection pooling allows **reusing a small set of pre-established database connections**

- **reducing the overhead** of constant connection setup and teardown.

Using psycopg2.pool:

```ruby
from psycopg2 import pool

# Initialize the connection pool globally
connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,  # min, max connections
  host=os.environ.get('POSTGRES_HOST', 'localhost'),
  database=os.environ.get('POSTGRES_DB', 'mydb'),
  user=os.environ.get('POSTGRES_USER', 'user'),
  password=os.environ.get('POSTGRES_PASSWORD', 'password'))

def get_db_connection():
  if connection_pool:
    return connection_pool.getconn()

def release_db_connection(conn):
  if connection_pool:
    connection_pool.putconn(conn)
...
```

### Benefits

- Connection pooling reuses connections, reducing the overhead of creating new ones.
- Helps prevent hitting connection limits on the database server.
- Helps improve performance in high-traffic situations.

# Useful commands

```ruby
docker image ls
REPOSITORY                                  TAG       IMAGE ID       CREATED             SIZE
10k-users-for-10m-records-flask             latest    6d116b2b33f7   17 minutes ago      156MB
10k-users-for-10m-records-flask_replica_2   latest    6afbf47cce3f   17 minutes ago      156MB
10k-users-for-10m-records-flask_replica_1   latest    3f7df984ce90   17 minutes ago      156MB
10k-users-for-10m-records-nginx             latest    67e6b00b8b18   About an hour ago   47MB
10k-users-for-10m-records-data-populator    latest    05edfd730fa4   21 hours ago        155MB
10k-users-for-10m-records-data-query        latest    3b7df6b4b1cb   21 hours ago        155MB
postgres                                    13        d76feacfc4a6   2 months ago        419MB
```

```ruby
docker image ls --format '{{.Repository}} {{.ID}}' | grep flask
10k-users-for-10m-records-flask 6d116b2b33f7
10k-users-for-10m-records-flask_replica_2 6afbf47cce3f
10k-users-for-10m-records-flask_replica_1 3f7df984ce90
```

```ruby
$ docker image rm $(docker image ls --format '{{.Repository}} {{.ID}}' | grep flask) -f
Untagged: 10k-users-for-10m-records-flask_replica_1:latest
Deleted: sha256:3f7df984ce90442566fbfaa7a00a580092ac7bb8b6ecf7ef94211c1c55bd2004
Untagged: 10k-users-for-10m-records-flask:latest
Deleted: sha256:6d116b2b33f7fef3f6ea97ae6f804b7eef331f52278c41e1a82661c694226ff5
Untagged: 10k-users-for-10m-records-flask_replica_2:latest
Deleted: sha256:6afbf47cce3f4ac2673f357dcbc883d8ffe5afcee74c334cd334a1d6c9133920
```

# Contribute

Got **something interesting** you'd like to **add or change**? Please feel free to [Open a Pull Request](https://github.com/juanroldan1989/10K-users-for-10M-records/pulls)

If you want to say **thank you** and/or support the active development of `10K Users for 10M records`:

1. Add a [GitHub Star](https://github.com/juanroldan1989/10K-users-for-10M-records/stargazers) to the project.
2. Tweet about the project [on your Twitter](https://twitter.com/intent/tweet?text=Hey%20I've%20just%20discovered%20this%20cool%20app%20on%20Github%20by%20@JhonnyDaNiro%20-%10K%20Users%2010M&url=https://github.com/juanroldan1989/10K-users-for-10M-records/&via=Github).
3. Write a review or tutorial on [Medium](https://medium.com), [Dev.to](https://dev.to) or personal blog.
