# Build the frontend using Node.js 14
FROM node:14 AS build-stage

# Setting the working directory in the container
WORKDIR /app

# Copying package.json to install only necessary dependencies
COPY package.json ./

# Installing dependencies
RUN npm install

# Copying the entire frontend codebase to the container
COPY . .

# Setting an environment variable for the API Gateway URL
ARG API_GATEWAY_URL
ENV API_GATEWAY=$API_GATEWAY_URL

# Running the build process for the frontend
RUN npm run build

#Serve the frontend using Nginx
FROM nginx:alpine AS serve-stage

# Copying the built frontend files from the build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Exposing port 80 for the application
EXPOSE 80

# Adding a health check to verify the service is running
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --spider -q http://localhost || exit 1

# Running Nginx to serve the frontend application
CMD ["nginx", "-g", "daemon off;"]
