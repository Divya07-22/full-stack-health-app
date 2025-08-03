# Stage 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application code into the container
COPY . .

# Expose the port the app will run on
EXPOSE 8080

# Define the command to run the application using Gunicorn
# This is the command that Render would have run for us.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
