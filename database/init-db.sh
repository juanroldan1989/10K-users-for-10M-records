#!/bin/bash
set -e

# Check if the database exists; if not, create it.
echo "Creating database mydb ..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
   CREATE DATABASE mydb;
EOSQL

echo "Database mydb created successfully!"
