# 🎯 Axie Studio Account Management System

## 📋 Overview

Your Axie Studio now has a complete commercial account management system with 600 pre-configured accounts across 3 tiers. This system is designed for selling pre-configured accounts instead of allowing user registration.

## 💰 Pricing Structure

### 🥉 Starter Tier (200 accounts) - $29/month
- **Accounts**: starter001@axiestudio.se to starter200@axiestudio.se
- **Limits**: 50 workflows, 5,000 API calls/month, 1GB storage
- **Support**: Email support
- **Revenue**: $5,800/month potential

### 🥈 Professional Tier (200 accounts) - $79/month  
- **Accounts**: professional001@axiestudio.se to professional200@axiestudio.se
- **Limits**: 200 workflows, 25,000 API calls/month, 10GB storage
- **Support**: Priority support
- **Revenue**: $15,800/month potential

### 🥇 Enterprise Tier (200 accounts) - $199/month
- **Accounts**: enterprise001@axiestudio.se to enterprise200@axiestudio.se
- **Limits**: Unlimited workflows, 100,000 API calls/month, 50GB storage
- **Support**: 24/7 support
- **Revenue**: $39,800/month potential

**Total Potential Revenue: $61,400/month**

## 🔧 System Components

### 1. Pre-configured Accounts
- ✅ 600 accounts generated with secure passwords
- ✅ Proper tier distribution (200 each)
- ✅ Account numbering system
- ✅ Easy CSV/JSON management

### 2. Admin Dashboard
- ✅ Account management interface at `/admin/accounts`
- ✅ User search and filtering
- ✅ Usage monitoring
- ✅ Account editing capabilities
- ✅ Export/import functionality

### 3. Tier-based Limits
- ✅ Workflow creation limits
- ✅ API call tracking and limits
- ✅ Storage usage monitoring
- ✅ Automatic enforcement

### 4. User Profile Management
- ✅ Users can change username/password
- ✅ View plan details and usage
- ✅ Usage progress indicators
- ✅ Plan information display

### 5. No Signup System
- ✅ Signup functionality completely removed
- ✅ Login-only access
- ✅ Registration API disabled
- ✅ Clean login experience

## 📁 File Structure

```
src/backend/base/axie_studio/
├── services/
│   ├── account_manager.py          # Account management service
│   └── tier_limits.py              # Tier limits enforcement
├── api/v1/
│   ├── accounts.py                 # Admin account API
│   └── profile.py                  # User profile API
├── scripts/
│   ├── generate_accounts.py        # Account generation
│   └── manage_accounts.py          # CLI management tool
└── accounts_data/
    ├── axie_studio_accounts.json   # Account data
    ├── axie_studio_accounts.csv    # Editable CSV
    └── accounts_summary.json       # Business summary

src/frontend/src/pages/
├── AdminPage/AccountsPage/         # Admin dashboard
├── ProfilePage/                    # User profile page
└── LoginPage/                      # Login only (no signup)
```

## 🚀 Getting Started

### 1. Import Accounts to Database
```bash
cd src/backend/base
python -m axie_studio.scripts.manage_accounts import
```

### 2. Access Admin Dashboard
- Login as admin: `stefan@axiestudio.se`
- Navigate to: `/admin/accounts`
- Manage all 600 accounts

### 3. Account Management CLI
```bash
# List all accounts
python -m axie_studio.scripts.manage_accounts list

# Export to CSV
python -m axie_studio.scripts.manage_accounts export

# Reset monthly usage
python -m axie_studio.scripts.manage_accounts reset-usage

# Validate account data
python -m axie_studio.scripts.manage_accounts validate
```

## 📊 Admin Features

### Account Management Dashboard
- **View all 600 accounts** with filtering
- **Search by username** or account number
- **Filter by tier** (Starter/Professional/Enterprise)
- **Filter by status** (Active/Inactive)
- **Edit account details** (username, tier, status)
- **Monitor usage** (workflows, API calls, storage)
- **Export/Import CSV** for bulk management

### Usage Monitoring
- **Real-time usage tracking** for all accounts
- **Tier limit enforcement** automatically applied
- **Monthly usage reset** functionality
- **Revenue tracking** and projections

## 👤 User Features

### Profile Management
- **Change username and password**
- **View current plan details**
- **Monitor usage quotas**
- **See tier limits and pricing**

### Automatic Limits
- **Workflow creation** blocked when limit reached
- **API calls** tracked and limited per month
- **Storage usage** monitored and enforced
- **Clear error messages** when limits exceeded

## 💼 Business Operations

### Selling Accounts
1. **Choose tier** based on customer needs
2. **Provide credentials** from CSV file
3. **Account is ready** immediately
4. **Customer logs in** and starts using

### Account Provisioning
1. **Edit CSV file** for bulk changes
2. **Import via admin dashboard**
3. **Or use CLI tools** for automation
4. **Accounts update** immediately

### Monthly Management
1. **Reset API usage** monthly
2. **Monitor revenue** potential
3. **Track active accounts**
4. **Export usage reports**

## 🔒 Security Features

- **Secure password generation** for all accounts
- **Admin-only account management**
- **User data isolation** (each user sees only their data)
- **Tier-based access control**
- **No public registration** (controlled access only)

## 📈 Revenue Tracking

The system tracks:
- **Total potential revenue**: $61,400/month
- **Active account revenue**: Based on active accounts
- **Tier distribution**: Revenue by plan type
- **Usage patterns**: To optimize pricing

## 🛠️ Customization

### Adding New Tiers
1. Update `UserTier` enum in `user/model.py`
2. Add limits to `TIER_LIMITS` dictionary
3. Update frontend tier colors and names
4. Regenerate accounts if needed

### Changing Limits
1. Edit `TIER_LIMITS` in `user/model.py`
2. Limits apply immediately to all users
3. No database migration needed

### Bulk Account Changes
1. Edit `accounts_data/axie_studio_accounts.csv`
2. Import via admin dashboard
3. Or use CLI import command

## 🎉 Success Metrics

Your Axie Studio commercial platform now has:
- ✅ **600 ready-to-sell accounts**
- ✅ **Complete admin management system**
- ✅ **Automatic tier limit enforcement**
- ✅ **User profile management**
- ✅ **No signup abuse potential**
- ✅ **Easy account provisioning**
- ✅ **Revenue tracking capabilities**

**You're ready to start selling Axie Studio accounts!** 🚀
