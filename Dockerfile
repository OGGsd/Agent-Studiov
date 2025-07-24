FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Expose the default Axie Studio port
EXPOSE 7860

# Set environment variables
ENV AXIE_STUDIO_HOST=0.0.0.0
ENV AXIE_STUDIO_PORT=7860

# Start the application
CMD ["axie-studio", "run"] 