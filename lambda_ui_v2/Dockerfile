# --- BUILD STAGE ---
# Use an official Node runtime as the parent image
FROM node:18.18 as build-stage

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

# Build the app for production
RUN npm run build

# --- SERVE STAGE ---
# Use a simple server to serve the built app
FROM nginx:1.24.0-alpine
# Copy from build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
# copy the nginx configuration file
COPY default.conf /etc/nginx/conf.d/default.conf
