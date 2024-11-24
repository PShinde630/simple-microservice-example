# Official MongoDB image with required binaries and services
FROM mongo:latest

# Setting environment variables for initial database setup
ENV MONGO_INITDB_DATABASE=quote_db
ENV MONGO_INITDB_ROOT_USERNAME=root
ENV MONGO_INITDB_ROOT_PASSWORD=pass

# Adding the initialization script to automatically load data at startup
COPY init-db.js /docker-entrypoint-initdb.d/init-db.js

# Adding a health check to monitor MongoDB service availability
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=5 \
  CMD mongo --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --eval "db.stats()" $MONGO_INITDB_DATABASE || exit 1
