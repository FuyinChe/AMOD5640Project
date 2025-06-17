# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file first for caching
COPY requirements.txt .

# Install system dependencies (if needed) and Python packages
RUN apt-get update && apt-get install -y build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the rest of your project files
COPY . .

# Expose port Railway expects
EXPOSE 8000

# Command to run your Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
