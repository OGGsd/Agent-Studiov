# 🚀 Axie Studio Production Deployment Guide

## ✅ Current Status
Your Axie Studio application has been successfully rebranded and is functional. However, several critical security and configuration issues must be addressed before production deployment.

## 🚨 Critical Security Issues (MUST FIX IMMEDIATELY)

### 1. Change Default Credentials
```bash
# Set secure credentials via environment variables
export AXIE_STUDIO_SUPERUSER="your_admin_username"
export AXIE_STUDIO_SUPERUSER_PASSWORD="your_very_secure_password_here"
```

### 2. Generate Secure Secret Key
```bash
# Generate a secure 256-bit secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
export AXIE_STUDIO_SECRET_KEY="your_generated_secret_key_here"
```

### 3. Configure Production Database
```bash
# Use PostgreSQL for production (not SQLite)
export AXIE_STUDIO_DATABASE_URL="postgresql://username:password@localhost:5432/axie_studio"
```

### 4. Configure Redis Cache
```bash
export AXIE_STUDIO_REDIS_URL="redis://localhost:6379/0"
export AXIE_STUDIO_CACHE_TYPE="redis"
```

## 🔧 Production Configuration

### Environment Variables
Create a `.env` file with these production settings:

```bash
# Security
AXIE_STUDIO_SECRET_KEY=your_256_bit_secret_key
AXIE_STUDIO_SUPERUSER=admin
AXIE_STUDIO_SUPERUSER_PASSWORD=your_secure_password

# Database
AXIE_STUDIO_DATABASE_URL=postgresql://user:pass@localhost:5432/axie_studio

# Cache
AXIE_STUDIO_CACHE_TYPE=redis
AXIE_STUDIO_REDIS_URL=redis://localhost:6379/0

# Security Settings
AXIE_STUDIO_AUTO_LOGIN=false
AXIE_STUDIO_NEW_USER_IS_ACTIVE=false

# Production Settings
AXIE_STUDIO_LOG_LEVEL=info
AXIE_STUDIO_WORKERS=4
AXIE_STUDIO_HOST=0.0.0.0
AXIE_STUDIO_PORT=7860

# Disable Development Features
AXIE_STUDIO_STORE=false
AXIE_STUDIO_DO_NOT_TRACK=true
AXIE_STUDIO_BACKEND_ONLY=false
```

## 🐳 Docker Deployment (Recommended)

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml ./
RUN pip install -e .

# Copy application code
COPY src/ ./src/

# Create non-root user
RUN useradd -m -u 1000 axie && chown -R axie:axie /app
USER axie

# Expose port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Start application
CMD ["axie-studio", "run", "--host", "0.0.0.0", "--port", "7860"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  axie-studio:
    build: .
    ports:
      - "7860:7860"
    environment:
      - AXIE_STUDIO_DATABASE_URL=postgresql://axie:password@postgres:5432/axie_studio
      - AXIE_STUDIO_REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: axie_studio
      POSTGRES_USER: axie
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - axie-studio
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

## 🔒 Security Hardening

### 1. SSL/TLS Configuration
```bash
# Generate SSL certificates (use Let's Encrypt for production)
certbot certonly --standalone -d yourdomain.com
```

### 2. Nginx Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    location / {
        proxy_pass http://axie-studio:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Firewall Configuration
```bash
# Allow only necessary ports
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw enable
```

## 📊 Monitoring & Logging

### 1. Enable Prometheus Metrics
```bash
export AXIE_STUDIO_PROMETHEUS_ENABLED=true
export AXIE_STUDIO_PROMETHEUS_PORT=9090
```

### 2. Configure Structured Logging
```bash
export AXIE_STUDIO_LOG_LEVEL=info
export AXIE_STUDIO_LOG_FILE=/app/logs/axie-studio.log
```

## 🚀 Deployment Steps

1. **Prepare Environment**
   ```bash
   git clone https://github.com/axiestudio/axie-studio.git
   cd axie-studio
   ```

2. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your production values
   ```

3. **Deploy with Docker**
   ```bash
   docker-compose up -d
   ```

4. **Verify Deployment**
   ```bash
   curl -f http://localhost:7860/health
   ```

## ⚠️ Known Issues & Limitations

1. **Package Dependencies**: Some dependencies may need version updates for production stability
2. **Frontend Assets**: Frontend may still contain Langflow references that need updating
3. **Database Migrations**: Ensure all Alembic migrations are applied in production
4. **API Keys**: Secure all third-party API keys in environment variables

## 📞 Support

For production deployment support, contact: support@axiestudio.se

---

**⚠️ WARNING**: Do not deploy to production without addressing all security issues listed above!
