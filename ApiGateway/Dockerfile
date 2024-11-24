# Use of a lightweight Node.js 18 image
FROM node:18-alpine

# Setting the working directory inside the container
WORKDIR /app

# Copying package files first for dependency installation
COPY package*.json ./

# Installing dependencies with minimal log output
RUN npm install --silent

# Copying the app source code
COPY . .

# Setting the appl port
ENV PORT=3000

# Exposing the appl port
EXPOSE $PORT

# Adding a health check to verify appl status
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --spider -q http://localhost:$PORT/api/status || exit 1

# Running the app
CMD ["node", "index.js"]
