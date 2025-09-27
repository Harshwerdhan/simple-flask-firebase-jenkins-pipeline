# Start from official Python base image
FROM python:3.12-slim

# Install python3-venv and other essentials
RUN apt-get update && \
    apt-get install -y python3-venv python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements.txt early to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies (optional)
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Default command (can be overridden in Jenkins)
CMD ["bash"]
