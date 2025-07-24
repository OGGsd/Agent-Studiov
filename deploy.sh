#!/bin/bash

# 🚀 Axie Studio Commercial Deployment Script
# Handles complete deployment including 600 pre-configured accounts

set -e  # Exit on any error

echo "🚀 Starting Axie Studio Commercial Deployment..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
    print_warning "Running as root. This is fine for deployment."
fi

# Step 1: Update system packages
print_status "Updating system packages..."
apt update && apt upgrade -y

# Step 2: Install required dependencies
print_status "Installing required dependencies..."
apt install -y python3 python3-pip python3-venv nodejs npm postgresql postgresql-contrib nginx git curl

# Step 3: Setup PostgreSQL if not already configured
print_status "Configuring PostgreSQL..."
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw axie_studio; then
    print_status "Creating PostgreSQL database and user..."
    sudo -u postgres createdb axie_studio
    sudo -u postgres psql -c "CREATE USER axie_studio_user WITH PASSWORD 'your_secure_password_here';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE axie_studio TO axie_studio_user;"
    print_success "PostgreSQL database created"
else
    print_success "PostgreSQL database already exists"
fi

# Step 4: Clone/Update repository
REPO_DIR="/opt/axie-studio"
if [ -d "$REPO_DIR" ]; then
    print_status "Updating existing repository..."
    cd $REPO_DIR
    git pull origin main
else
    print_status "Cloning repository..."
    git clone https://github.com/OGGsd/agent-studiov.git $REPO_DIR
    cd $REPO_DIR
fi

# Step 5: Setup Python virtual environment
print_status "Setting up Python virtual environment..."
cd $REPO_DIR
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Step 6: Install Python dependencies
print_status "Installing Python dependencies..."
cd src/backend/base
pip install -r requirements.txt

# Step 7: Setup environment variables
print_status "Setting up environment variables..."
cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://axie_studio_user:your_secure_password_here@localhost/axie_studio

# Security
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin Configuration
ADMIN_EMAIL=stefan@axiestudio.se
ADMIN_PASSWORD=STEfanjohn!12

# Application Settings
DEBUG=False
ENVIRONMENT=production
EOF

# Step 8: Run database migrations
print_status "Running database migrations..."
python -m alembic upgrade head

# Step 9: 🎯 IMPORT PRE-CONFIGURED ACCOUNTS
print_status "Importing 600 pre-configured commercial accounts..."
python -m axie_studio.scripts.manage_accounts import

if [ $? -eq 0 ]; then
    print_success "✅ Successfully imported 600 accounts!"
    print_success "   • 200 Starter accounts ($29/month)"
    print_success "   • 200 Professional accounts ($79/month)" 
    print_success "   • 200 Enterprise accounts ($199/month)"
    print_success "   • Total potential revenue: $61,400/month"
else
    print_error "❌ Failed to import accounts"
    exit 1
fi

# Step 10: Build frontend
print_status "Building frontend..."
cd $REPO_DIR/src/frontend
npm install
npm run build

# Step 11: Setup Nginx configuration
print_status "Configuring Nginx..."
cat > /etc/nginx/sites-available/axie-studio << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Frontend static files
    location / {
        root /opt/axie-studio/src/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API endpoints
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin endpoints
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable the site
ln -sf /etc/nginx/sites-available/axie-studio /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

# Step 12: Setup systemd service for the backend
print_status "Setting up systemd service..."
cat > /etc/systemd/system/axie-studio.service << EOF
[Unit]
Description=Axie Studio Backend
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=$REPO_DIR/src/backend/base
Environment=PATH=$REPO_DIR/venv/bin
ExecStart=$REPO_DIR/venv/bin/python -m uvicorn axie_studio.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Step 13: Start and enable services
print_status "Starting services..."
systemctl daemon-reload
systemctl enable axie-studio
systemctl start axie-studio
systemctl enable nginx
systemctl start nginx
systemctl enable postgresql
systemctl start postgresql

# Step 14: Verify deployment
print_status "Verifying deployment..."
sleep 5

if systemctl is-active --quiet axie-studio; then
    print_success "✅ Axie Studio backend is running"
else
    print_error "❌ Axie Studio backend failed to start"
    systemctl status axie-studio
    exit 1
fi

if systemctl is-active --quiet nginx; then
    print_success "✅ Nginx is running"
else
    print_error "❌ Nginx failed to start"
    exit 1
fi

# Step 15: Display account statistics
print_status "Displaying account statistics..."
cd $REPO_DIR/src/backend/base
source $REPO_DIR/venv/bin/activate
python -m axie_studio.scripts.manage_accounts list

# Step 16: Setup SSL (optional but recommended)
print_status "Setting up SSL certificate..."
if command -v certbot &> /dev/null; then
    print_status "Certbot found, setting up SSL..."
    certbot --nginx -d your-domain.com -d www.your-domain.com --non-interactive --agree-tos --email stefan@axiestudio.se
    print_success "✅ SSL certificate installed"
else
    print_warning "Certbot not found. Install with: apt install certbot python3-certbot-nginx"
    print_warning "Then run: certbot --nginx -d your-domain.com"
fi

# Step 17: Setup log rotation
print_status "Setting up log rotation..."
cat > /etc/logrotate.d/axie-studio << EOF
/var/log/axie-studio/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload axie-studio
    endscript
}
EOF

# Step 18: Create backup script
print_status "Creating backup script..."
cat > /opt/backup-axie-studio.sh << 'EOF'
#!/bin/bash
# Backup script for Axie Studio
BACKUP_DIR="/opt/backups/axie-studio"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U axie_studio_user -h localhost axie_studio > $BACKUP_DIR/database_$DATE.sql

# Backup account data
cp -r /opt/axie-studio/src/backend/base/accounts_data $BACKUP_DIR/accounts_data_$DATE

# Keep only last 7 days of backups
find $BACKUP_DIR -name "database_*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "accounts_data_*" -mtime +7 -exec rm -rf {} \;

echo "Backup completed: $DATE"
EOF

chmod +x /opt/backup-axie-studio.sh

# Add to crontab for daily backups
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/backup-axie-studio.sh") | crontab -

print_success "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "=================================================="
print_success "✅ Axie Studio Commercial Platform is now live!"
echo ""
print_success "🎯 WHAT'S READY:"
print_success "   • 600 pre-configured accounts imported"
print_success "   • Admin dashboard: http://your-domain.com/admin"
print_success "   • Account management: http://your-domain.com/admin/accounts"
print_success "   • User login: http://your-domain.com/login"
print_success "   • API endpoints: http://your-domain.com/api"
echo ""
print_success "🔑 ADMIN LOGIN:"
print_success "   • Email: stefan@axiestudio.se"
print_success "   • Password: STEfanjohn!12"
echo ""
print_success "💰 BUSINESS READY:"
print_success "   • 200 Starter accounts ready to sell ($29/month)"
print_success "   • 200 Professional accounts ready to sell ($79/month)"
print_success "   • 200 Enterprise accounts ready to sell ($199/month)"
print_success "   • Total potential revenue: $61,400/month"
echo ""
print_success "🛠️ MANAGEMENT:"
print_success "   • Account CLI: cd /opt/axie-studio/src/backend/base && python -m axie_studio.scripts.manage_accounts"
print_success "   • Service status: systemctl status axie-studio"
print_success "   • Logs: journalctl -u axie-studio -f"
print_success "   • Daily backups: /opt/backup-axie-studio.sh"
echo ""
print_success "🚀 YOUR COMMERCIAL AXIE STUDIO IS READY TO GENERATE REVENUE!"
