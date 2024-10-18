# Start from a lightweight Nginx image
FROM nginx:alpine

# Create a non-root user and group
RUN addgroup -S appgroup && adduser -S nonrootuser -G appgroup

# Ensure the non-root user can write to the required Nginx directories to avoid issues:
# 1) nginx: [emerg] mkdir() "/var/cache/nginx/client_temp" failed (13: Permission denied)
# 2) nginx: [emerg] open() "/var/run/nginx.pid" failed (13: Permission denied)
RUN mkdir -p /var/cache/nginx/client_temp /var/run && \
  chown -R nonrootuser:appgroup /var/cache/nginx /var/run

# Copy Nginx configuration files
COPY --chown=nonrootuser:appgroup default.conf /etc/nginx/conf.d/default.conf
COPY --chown=nonrootuser:appgroup nginx.conf /etc/nginx/nginx.conf

# Set the working directory
WORKDIR /app

# Change ownership of the working directory to the non-root user
RUN chown -R nonrootuser:appgroup /app

# Switch to the non-root user
USER nonrootuser

# Expose necessary port
EXPOSE 80

# Use the default Nginx command to start
CMD ["nginx", "-g", "daemon off;"]