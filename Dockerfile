# Dockerfile

# Stage 1: Build the application with pre-loaded models
# Use a slim Python base image
FROM python:3.9-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Install system dependencies that might be needed for libraries like OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- This is the key step for pre-loading models ---
# Copy the pre-loading script and run it. This will download and cache the models.
COPY preload_models.py .
RUN python preload_models.py

# Copy the rest of your application code
COPY main.py .

# Expose the port the app will run on. Render provides the PORT env var.
# We'll use 10000 as a default.
EXPOSE 10000

# The command to run your application using Gunicorn (a production-ready server)
# It listens on the port provided by Render's PORT environment variable.
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:10000"]