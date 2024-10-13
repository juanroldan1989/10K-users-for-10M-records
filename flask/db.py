import os
import psycopg2
from psycopg2 import pool

# Environment variables
USE_POOLING = os.environ.get('USE_POOLING', 'false').lower() == 'true'
POOL_MINCONN = int(os.environ.get('POOL_MINCONN', 1))  # Minimum connections in pool
POOL_MAXCONN = int(os.environ.get('POOL_MAXCONN', 10))  # Maximum connections in pool

# Global connection pool (initialize once per Flask instance)
connection_pool = None

def initialize_pool():
  global connection_pool
  if connection_pool is None:
    try:
      connection_pool = pool.SimpleConnectionPool(
        minconn=POOL_MINCONN,
        maxconn=POOL_MAXCONN,
        host=os.environ.get('POSTGRES_HOST'),
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
      )
      print(f"Connection pooling enabled: minconn={POOL_MINCONN}, maxconn={POOL_MAXCONN}")
    except psycopg2.OperationalError as e:
      print(f"Error creating connection pool: {e}")
      connection_pool = None
      print(f"Connection pooling enabled: minconn={os.environ.get('POOL_MINCONN', 1)}, maxconn={os.environ.get('POOL_MAXCONN', 10)}")

# Function to get a database connection (pooled or direct)
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

# Function to return a pooled connection back to the pool
def release_db_connection(conn):
  if USE_POOLING and connection_pool:
    print("Connection returned to the pool")
    connection_pool.putconn(conn)
  else:
    print("Connection closed")
    conn.close()

# Function to close the pool when the app shuts down
def close_connection_pool():
  if connection_pool:
    print("Connection pool closed")
    connection_pool.closeall()
