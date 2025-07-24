# 🚀 Axie Studio Commercial Deployment Guide

## 📋 Overview

This guide provides **automated deployment scripts** that will:
- ✅ Deploy your Axie Studio platform
- ✅ **Automatically import all 600 pre-configured accounts**
- ✅ Set up admin dashboard and account management
- ✅ Configure tier-based limits
- ✅ Make your platform ready for commercial sales

## 🎯 Deployment Options

### Option 1: DigitalOcean App Platform (RECOMMENDED)

**Perfect for your current setup!**

#### Step 1: Update your DigitalOcean App Spec
Add this to your app spec or create a new build command:

```yaml
name: axie-studio
services:
- name: web
  source_dir: /
  github:
    repo: OGGsd/agent-studiov
    branch: main
  run_command: ./digitalocean-deploy.sh
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  routes:
  - path: /
```

#### Step 2: Deploy
- Push your code (already done ✅)
- DigitalOcean will automatically run `digitalocean-deploy.sh`
- **All 600 accounts will be imported automatically!**

### Option 2: Traditional VPS/Server

#### Step 1: SSH into your server
```bash
ssh root@your-server-ip
```

#### Step 2: Clone and deploy
```bash
git clone https://github.com/OGGsd/agent-studiov.git
cd agent-studiov
chmod +x deploy.sh
./deploy.sh
```

## 🎯 What the Deployment Scripts Do

### 🔧 **Automatic Account Import:**
```bash
# This happens automatically during deployment:
python -m axie_studio.scripts.manage_accounts import

# Results in:
✅ 200 Starter accounts (starter001@axiestudio.se to starter200@axiestudio.se)
✅ 200 Professional accounts (professional001@axiestudio.se to professional200@axiestudio.se)  
✅ 200 Enterprise accounts (enterprise001@axiestudio.se to enterprise200@axiestudio.se)
```

### 🎊 **Complete Setup:**
- Database migrations
- Account import
- Admin user creation
- Frontend build
- Service configuration
- SSL setup (full deployment)

## 🔍 Verification After Deployment

### Check if accounts were imported:
```bash
# SSH into your server and run:
cd /path/to/axie-studio/src/backend/base
python -m axie_studio.scripts.manage_accounts list
```

### Expected output:
```
📊 ACCOUNT SUMMARY
Total Accounts: 600
Active Accounts: 600
Potential Revenue: $61,400/month

📋 TIER BREAKDOWN:
  STARTER:
    • Count: 200 accounts
    • Price: $29/month
    • Revenue: $5,800/month
  PROFESSIONAL:
    • Count: 200 accounts  
    • Price: $79/month
    • Revenue: $15,800/month
  ENTERPRISE:
    • Count: 200 accounts
    • Price: $199/month
    • Revenue: $39,800/month
```

## 🎯 Post-Deployment Access

### Admin Dashboard:
- **URL**: `https://your-app.ondigitalocean.app/admin`
- **Login**: `stefan@axiestudio.se`
- **Password**: `STEfanjohn!12`

### Account Management:
- **URL**: `https://your-app.ondigitalocean.app/admin/accounts`
- **Features**: View, edit, search all 600 accounts

### User Login:
- **URL**: `https://your-app.ondigitalocean.app/login`
- **Accounts**: Any of the 600 pre-configured accounts

## 💰 Start Selling Immediately

### Account Credentials Available:
```
Starter Accounts:
- starter001@axiestudio.se (password in CSV)
- starter002@axiestudio.se (password in CSV)
- ... up to starter200@axiestudio.se

Professional Accounts:  
- professional001@axiestudio.se (password in CSV)
- professional002@axiestudio.se (password in CSV)
- ... up to professional200@axiestudio.se

Enterprise Accounts:
- enterprise001@axiestudio.se (password in CSV)
- enterprise002@axiestudio.se (password in CSV)  
- ... up to enterprise200@axiestudio.se
```

### Get Account Passwords:
```bash
# Export CSV with all account details:
python -m axie_studio.scripts.manage_accounts export --output accounts_for_sales.csv
```

## 🛠️ Management Commands

### Account Management:
```bash
# List all accounts
python -m axie_studio.scripts.manage_accounts list

# Export accounts to CSV
python -m axie_studio.scripts.manage_accounts export

# Reset monthly usage (run monthly)
python -m axie_studio.scripts.manage_accounts reset-usage

# Validate account data
python -m axie_studio.scripts.manage_accounts validate
```

### Service Management:
```bash
# Check service status
systemctl status axie-studio

# View logs
journalctl -u axie-studio -f

# Restart service
systemctl restart axie-studio
```

## 🚨 Troubleshooting

### If accounts didn't import:
```bash
# Manually import accounts:
cd src/backend/base
python -m axie_studio.scripts.manage_accounts import
```

### If admin can't login:
```bash
# Recreate admin user:
python -c "
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from axie_studio.services.database.models.user.model import User
from axie_studio.services.auth.utils import get_password_hash
from axie_studio.services.deps import get_settings

settings = get_settings()
engine = create_engine(str(settings.database_url))
SessionLocal = sessionmaker(bind=engine)

with SessionLocal() as session:
    admin = session.query(User).filter(User.username == 'stefan@axiestudio.se').first()
    if admin:
        admin.password = get_password_hash('STEfanjohn!12')
        admin.is_superuser = True
        session.commit()
        print('Admin password reset')
"
```

## 🎉 Success Indicators

### ✅ Deployment Successful When:
- [ ] 600 accounts imported
- [ ] Admin dashboard accessible
- [ ] Account management working
- [ ] User login functional
- [ ] Tier limits enforced

### 💰 Ready for Business When:
- [ ] Can login to admin dashboard
- [ ] Can see all 600 accounts in `/admin/accounts`
- [ ] Can export account CSV for sales team
- [ ] Customer accounts work with tier limits
- [ ] Revenue tracking shows $61,400 potential

## 🚀 Next Steps

1. **Test the deployment** - Login as admin and verify accounts
2. **Export account CSV** - Get credentials for your sales team  
3. **Start selling accounts** - Each customer gets instant access
4. **Monitor usage** - Track revenue and account utilization
5. **Scale up** - Add more accounts as needed

**Your commercial Axie Studio platform is ready to generate $61,400/month in revenue!** 🎊
