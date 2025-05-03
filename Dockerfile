# Use minimal Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional: needed for building some wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements file first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose PyWebIO default port
EXPOSE 8080

# Default command to run the app
CMD ["python", "bulls_web.py"]
