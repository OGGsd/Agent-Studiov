FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies using uv
RUN uv sync --frozen

# Expose the default Axie Studio port
EXPOSE 7860

# Set environment variables
ENV AXIE_STUDIO_HOST=0.0.0.0
ENV AXIE_STUDIO_PORT=7860

# Start the application
CMD ["uv", "run", "axie-studio", "run", "--host", "0.0.0.0", "--port", "7860"]