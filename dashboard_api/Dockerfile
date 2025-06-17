# Use base Python 3.12 slim image
FROM python:3.12-slim

# Install build dependencies (required for mysqlclient)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*    

# Set working directory to Django project root
WORKDIR /opt/app/dashboard_api

# Copy requirements.txt to working directory
COPY dashboard_api/requirements.txt .

# Create a virtual environment and install dependencies
RUN python -m venv --copies /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Activate virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy all project files into the working directory
COPY dashboard_api/ .

# Set Django settings module (if needed)
ENV DJANGO_SETTINGS_MODULE=dashboard_api.settings

# Set application port for Railway
ENV PORT=8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
