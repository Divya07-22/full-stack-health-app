# --- Stage 1: Build the React application ---
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . ./

# Build the React app for production
RUN npm run build

# --- Stage 2: Serve the built application with Nginx ---
FROM nginx:1.21.3-alpine

# Copy the built files from the 'build' stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for the Nginx web server
EXPOSE 80

# The container will automatically start Nginx
CMD ["nginx", "-g", "daemon off;"]
