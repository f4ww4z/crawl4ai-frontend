# Use Python 3.10 as base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Configure Poetry to not create virtual environment inside container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

RUN playwright install

RUN playwright install-deps

# Copy application files
COPY main.py .
COPY static/ static/

# Create directory for temporary files
RUN mkdir -p /app/output

# Expose port 8000
EXPOSE 8000

# Set the entry command
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
