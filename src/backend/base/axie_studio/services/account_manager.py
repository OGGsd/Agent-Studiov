"""
Account Manager Service for Pre-configured Commercial Accounts
Handles creation, management, and limits enforcement for 600 pre-configured accounts.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from axie_studio.services.database.models.user.model import (
    User, UserCreate, UserTier, TIER_LIMITS, TierLimits
)
from axie_studio.services.auth.utils import get_password_hash


class AccountManager:
    """Manages pre-configured commercial accounts."""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.accounts_file = Path("accounts_data/axie_studio_accounts.json")
    
    def load_accounts_from_file(self) -> List[Dict]:
        """Load accounts from JSON file."""
        if not self.accounts_file.exists():
            raise FileNotFoundError(f"Accounts file not found: {self.accounts_file}")
        
        with open(self.accounts_file, 'r') as f:
            return json.load(f)
    
    def create_accounts_in_database(self) -> Dict[str, int]:
        """Create all pre-configured accounts in the database."""
        accounts_data = self.load_accounts_from_file()
        created_count = 0
        skipped_count = 0
        
        for account_data in accounts_data:
            # Check if account already exists
            existing_user = self.db.query(User).filter(
                User.username == account_data["username"]
            ).first()
            
            if existing_user:
                skipped_count += 1
                continue
            
            # Create new user
            user_create = UserCreate(
                username=account_data["username"],
                password=get_password_hash(account_data["password"]),
                tier=UserTier(account_data["tier"]),
                account_number=account_data["account_number"]
            )
            
            new_user = User(
                username=user_create.username,
                password=user_create.password,
                tier=user_create.tier,
                account_number=user_create.account_number,
                is_active=True,
                is_superuser=False,
                api_calls_used_this_month=0,
                storage_used_gb=0.0
            )
            
            self.db.add(new_user)
            created_count += 1
        
        self.db.commit()
        
        return {
            "created": created_count,
            "skipped": skipped_count,
            "total": len(accounts_data)
        }
    
    def get_user_limits(self, user: User) -> TierLimits:
        """Get limits for a user based on their tier."""
        return TIER_LIMITS[user.tier]
    
    def check_workflow_limit(self, user: User) -> bool:
        """Check if user can create more workflows."""
        limits = self.get_user_limits(user)
        if limits.max_workflows == -1:  # Unlimited
            return True
        
        current_workflows = len(user.flows)
        return current_workflows < limits.max_workflows
    
    def check_api_call_limit(self, user: User, calls_to_add: int = 1) -> bool:
        """Check if user can make more API calls this month."""
        limits = self.get_user_limits(user)
        return (user.api_calls_used_this_month + calls_to_add) <= limits.max_api_calls_per_month
    
    def check_storage_limit(self, user: User, storage_to_add_gb: float = 0) -> bool:
        """Check if user can use more storage."""
        limits = self.get_user_limits(user)
        return (user.storage_used_gb + storage_to_add_gb) <= limits.max_storage_gb
    
    def increment_api_calls(self, user: User, count: int = 1) -> bool:
        """Increment user's API call count if within limits."""
        if not self.check_api_call_limit(user, count):
            return False
        
        user.api_calls_used_this_month += count
        self.db.commit()
        return True
    
    def update_storage_usage(self, user: User, new_usage_gb: float) -> bool:
        """Update user's storage usage if within limits."""
        if not self.check_storage_limit(user, new_usage_gb - user.storage_used_gb):
            return False
        
        user.storage_used_gb = new_usage_gb
        self.db.commit()
        return True
    
    def reset_monthly_usage(self) -> int:
        """Reset API call usage for all users (run monthly)."""
        users = self.db.query(User).all()
        reset_count = 0
        
        for user in users:
            user.api_calls_used_this_month = 0
            reset_count += 1
        
        self.db.commit()
        return reset_count
    
    def get_account_statistics(self) -> Dict:
        """Get statistics about all accounts."""
        stats = {
            "total_accounts": 0,
            "active_accounts": 0,
            "tiers": {},
            "usage_summary": {
                "total_api_calls": 0,
                "total_storage_gb": 0,
                "total_workflows": 0
            }
        }
        
        users = self.db.query(User).all()
        stats["total_accounts"] = len(users)
        
        for tier in UserTier:
            tier_users = [u for u in users if u.tier == tier]
            stats["tiers"][tier.value] = {
                "count": len(tier_users),
                "active": len([u for u in tier_users if u.is_active]),
                "total_api_calls": sum(u.api_calls_used_this_month for u in tier_users),
                "total_storage": sum(u.storage_used_gb for u in tier_users),
                "total_workflows": sum(len(u.flows) for u in tier_users)
            }
        
        stats["active_accounts"] = len([u for u in users if u.is_active])
        stats["usage_summary"]["total_api_calls"] = sum(u.api_calls_used_this_month for u in users)
        stats["usage_summary"]["total_storage_gb"] = sum(u.storage_used_gb for u in users)
        stats["usage_summary"]["total_workflows"] = sum(len(u.flows) for u in users)
        
        return stats
    
    def export_accounts_csv(self, filepath: str) -> int:
        """Export all accounts to CSV for easy editing."""
        users = self.db.query(User).all()
        
        fieldnames = [
            'id', 'username', 'tier', 'account_number', 'is_active', 
            'api_calls_used_this_month', 'storage_used_gb', 'workflow_count',
            'created_at', 'last_login_at'
        ]
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for user in users:
                writer.writerow({
                    'id': str(user.id),
                    'username': user.username,
                    'tier': user.tier.value,
                    'account_number': user.account_number,
                    'is_active': user.is_active,
                    'api_calls_used_this_month': user.api_calls_used_this_month,
                    'storage_used_gb': user.storage_used_gb,
                    'workflow_count': len(user.flows),
                    'created_at': user.create_at.isoformat(),
                    'last_login_at': user.last_login_at.isoformat() if user.last_login_at else None
                })
        
        return len(users)
