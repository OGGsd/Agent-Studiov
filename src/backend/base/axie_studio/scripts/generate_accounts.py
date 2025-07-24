#!/usr/bin/env python3
"""
Script to generate 600 pre-configured accounts for Axie Studio commercial platform.
200 accounts per tier: Starter, Professional, Enterprise
"""

import json
import csv
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from axie_studio.services.database.models.user.model import UserTier, TIER_LIMITS


def generate_secure_password(length: int = 12) -> str:
    """Generate a secure random password."""
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_accounts() -> List[Dict]:
    """Generate 600 pre-configured accounts."""
    accounts = []
    account_id = 1
    
    # Generate accounts for each tier
    for tier in [UserTier.STARTER, UserTier.PROFESSIONAL, UserTier.ENTERPRISE]:
        tier_limits = TIER_LIMITS[tier]
        
        for i in range(1, 201):  # 200 accounts per tier
            account_number = f"{i:03d}"  # 001, 002, etc.
            username = f"{tier.value}{account_number}@axiestudio.se"
            password = generate_secure_password()
            
            account = {
                "id": account_id,
                "username": username,
                "password": password,  # Will be hashed when inserted into DB
                "tier": tier.value,
                "account_number": int(f"{['starter', 'professional', 'enterprise'].index(tier.value) + 1}{account_number}"),
                "is_active": True,
                "is_superuser": False,
                "max_workflows": tier_limits.max_workflows,
                "max_api_calls_per_month": tier_limits.max_api_calls_per_month,
                "max_storage_gb": tier_limits.max_storage_gb,
                "support_level": tier_limits.support_level,
                "price_per_month": tier_limits.price_per_month,
                "api_calls_used_this_month": 0,
                "storage_used_gb": 0.0,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "status": "available"  # available, sold, suspended
            }
            
            accounts.append(account)
            account_id += 1
    
    return accounts


def save_accounts_json(accounts: List[Dict], filepath: str):
    """Save accounts to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(accounts, f, indent=2, default=str)
    print(f"✅ Saved {len(accounts)} accounts to {filepath}")


def save_accounts_csv(accounts: List[Dict], filepath: str):
    """Save accounts to CSV file for easy editing."""
    if not accounts:
        return
    
    fieldnames = accounts[0].keys()
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(accounts)
    print(f"✅ Saved {len(accounts)} accounts to {filepath}")


def create_tier_summary(accounts: List[Dict]) -> Dict:
    """Create a summary of accounts by tier."""
    summary = {
        "total_accounts": len(accounts),
        "tiers": {},
        "potential_monthly_revenue": 0
    }
    
    for tier in [UserTier.STARTER, UserTier.PROFESSIONAL, UserTier.ENTERPRISE]:
        tier_accounts = [acc for acc in accounts if acc["tier"] == tier.value]
        tier_limits = TIER_LIMITS[tier]
        
        summary["tiers"][tier.value] = {
            "count": len(tier_accounts),
            "price_per_month": tier_limits.price_per_month,
            "max_revenue": len(tier_accounts) * tier_limits.price_per_month,
            "limits": {
                "workflows": tier_limits.max_workflows,
                "api_calls": tier_limits.max_api_calls_per_month,
                "storage_gb": tier_limits.max_storage_gb,
                "support": tier_limits.support_level
            }
        }
        
        summary["potential_monthly_revenue"] += summary["tiers"][tier.value]["max_revenue"]
    
    return summary


def main():
    """Main function to generate and save accounts."""
    print("🚀 Generating 600 pre-configured Axie Studio accounts...")
    
    # Create output directory
    output_dir = Path("accounts_data")
    output_dir.mkdir(exist_ok=True)
    
    # Generate accounts
    accounts = generate_accounts()
    
    # Save in multiple formats
    save_accounts_json(accounts, output_dir / "axie_studio_accounts.json")
    save_accounts_csv(accounts, output_dir / "axie_studio_accounts.csv")
    
    # Create summary
    summary = create_tier_summary(accounts)
    save_accounts_json(summary, output_dir / "accounts_summary.json")
    
    # Print summary
    print("\n📊 ACCOUNT GENERATION SUMMARY:")
    print(f"Total Accounts: {summary['total_accounts']}")
    print(f"Potential Monthly Revenue: ${summary['potential_monthly_revenue']:,}")
    print("\nTier Breakdown:")
    
    for tier_name, tier_data in summary["tiers"].items():
        print(f"  {tier_name.upper()}:")
        print(f"    • Count: {tier_data['count']} accounts")
        print(f"    • Price: ${tier_data['price_per_month']}/month")
        print(f"    • Max Revenue: ${tier_data['max_revenue']:,}/month")
        print(f"    • Limits: {tier_data['limits']['workflows']} workflows, "
              f"{tier_data['limits']['api_calls']:,} API calls, "
              f"{tier_data['limits']['storage_gb']}GB storage")
    
    print(f"\n✅ All files saved to: {output_dir.absolute()}")
    print("\n🎯 Next steps:")
    print("1. Review the generated accounts in the CSV file")
    print("2. Import accounts into the database")
    print("3. Set up admin dashboard for account management")


if __name__ == "__main__":
    main()
