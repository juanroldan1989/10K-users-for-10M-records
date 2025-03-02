# Use an official Python runtime as a base image
FROM python:3.9-slim

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup nonrootuser

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for PostgreSQL connection
# POSTGRES_HOST -> <your_rds_endpoint>
ENV POSTGRES_HOST=db
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=mydb

# Custom values for the data-populator script
ENV BATCH_SIZE=1000
ENV TOTAL_RECORDS=10000

# Change ownership of /app to the non-root user
RUN chown -R nonrootuser:appgroup /app

# Switch to the non-root user
USER nonrootuser

# Make port 5432 available to the world outside this container (if needed)
EXPOSE 5432

# Run the Python script
CMD ["python", "query_db.py"]