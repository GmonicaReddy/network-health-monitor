# Use Python 3.10 base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install ping, traceroute, and DNS tools
RUN apt-get update && apt-get install -y iputils-ping dnsutils traceroute && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create logs directory
RUN mkdir -p logs

# Default command (you can override this at runtime)
CMD ["python", "monitor.py", "google.com", "8.8.8.8"]
