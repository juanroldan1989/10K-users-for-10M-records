# Dockerfile definition includeds initialization script `init-db.sh`:
# This approach allows for a custom Docker image with an initialization script included.
# The script will be executed when the container is started, and it will create the necessary database.

FROM postgres:13

# Copy the initialization script into the container
COPY /database/init-db.sh /docker-entrypoint-initdb.d/init-db.sh

# Ensure the script has the correct permissions
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

# Entry point will trigger both PostgreSQL and the script execution
ENTRYPOINT ["docker-entrypoint.sh", "postgres"]