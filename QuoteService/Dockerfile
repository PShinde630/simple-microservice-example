# Slim version of Python 3.8 for lightweight containerization
FROM python:3.8-slim

# Setting the working directory inside the container to /app
WORKDIR /app

# Copying the app code into the container
COPY . .

# Installing required dependencies using pip with no-cache to reduce image size
RUN pip install --no-cache-dir flask pymongo redis

# Exposing port 5000 to allow communication between the container and the host
EXPOSE 5000

# Setting environment variable for Flask application entry point
ENV FLASK_APP=main.py

# Adding a health check to ensure Flask app is running
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl --fail http://localhost:5000/api/status || exit 1

# Starting the Flask application, accessible on all interfaces
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
