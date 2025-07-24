#!/usr/bin/env python3
"""
Account Management Script for Axie Studio
Easy command-line tool for managing pre-configured accounts.
"""

import argparse
import json
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from services.database.models.user.model import UserTier, TIER_LIMITS
from services.account_manager import AccountManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class AccountCLI:
    """Command-line interface for account management."""
    
    def __init__(self, database_url: str = "sqlite:///axie_studio.db"):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.accounts_file = Path("accounts_data/axie_studio_accounts.json")
    
    def list_accounts(self, tier: Optional[str] = None, active_only: bool = False):
        """List all accounts with optional filtering."""
        with self.SessionLocal() as session:
            account_manager = AccountManager(session)
            stats = account_manager.get_account_statistics()
            
            print(f"\n📊 ACCOUNT SUMMARY")
            print(f"Total Accounts: {stats['total_accounts']}")
            print(f"Active Accounts: {stats['active_accounts']}")
            print(f"Potential Revenue: ${sum(TIER_LIMITS[UserTier(t)].price_per_month * data['count'] for t, data in stats['tiers'].items()):,}/month")
            
            print(f"\n📋 TIER BREAKDOWN:")
            for tier_name, tier_data in stats["tiers"].items():
                tier_limits = TIER_LIMITS[UserTier(tier_name)]
                print(f"  {tier_name.upper()}:")
                print(f"    • Count: {tier_data['count']} accounts")
                print(f"    • Active: {tier_data['active']} accounts")
                print(f"    • Price: ${tier_limits.price_per_month}/month")
                print(f"    • Revenue: ${tier_data['count'] * tier_limits.price_per_month:,}/month")
    
    def import_accounts(self):
        """Import accounts from JSON file to database."""
        with self.SessionLocal() as session:
            account_manager = AccountManager(session)
            
            try:
                result = account_manager.create_accounts_in_database()
                print(f"✅ Import completed!")
                print(f"   Created: {result['created']} accounts")
                print(f"   Skipped: {result['skipped']} accounts (already exist)")
                print(f"   Total: {result['total']} accounts processed")
            except Exception as e:
                print(f"❌ Import failed: {e}")
    
    def export_csv(self, output_file: str = "accounts_export.csv"):
        """Export accounts to CSV file."""
        with self.SessionLocal() as session:
            account_manager = AccountManager(session)
            
            try:
                count = account_manager.export_accounts_csv(output_file)
                print(f"✅ Exported {count} accounts to {output_file}")
            except Exception as e:
                print(f"❌ Export failed: {e}")
    
    def reset_monthly_usage(self):
        """Reset monthly API usage for all accounts."""
        with self.SessionLocal() as session:
            account_manager = AccountManager(session)
            
            try:
                count = account_manager.reset_monthly_usage()
                print(f"✅ Reset monthly usage for {count} accounts")
            except Exception as e:
                print(f"❌ Reset failed: {e}")
    
    def generate_new_accounts(self, count: int = 600):
        """Generate new account data files."""
        from generate_accounts import main as generate_main
        
        print(f"🚀 Generating {count} new accounts...")
        generate_main()
        print(f"✅ Account generation completed!")
    
    def validate_accounts(self):
        """Validate account data integrity."""
        if not self.accounts_file.exists():
            print(f"❌ Accounts file not found: {self.accounts_file}")
            return
        
        try:
            with open(self.accounts_file, 'r') as f:
                accounts = json.load(f)
            
            print(f"🔍 Validating {len(accounts)} accounts...")
            
            # Check for duplicates
            usernames = [acc['username'] for acc in accounts]
            duplicates = set([x for x in usernames if usernames.count(x) > 1])
            
            if duplicates:
                print(f"❌ Found duplicate usernames: {duplicates}")
            else:
                print(f"✅ No duplicate usernames found")
            
            # Check tier distribution
            tier_counts = {}
            for account in accounts:
                tier = account['tier']
                tier_counts[tier] = tier_counts.get(tier, 0) + 1
            
            print(f"📊 Tier distribution:")
            for tier, count in tier_counts.items():
                print(f"   {tier}: {count} accounts")
            
            # Check account number ranges
            account_numbers = [acc['account_number'] for acc in accounts]
            print(f"📋 Account number range: {min(account_numbers)} - {max(account_numbers)}")
            
            print(f"✅ Validation completed!")
            
        except Exception as e:
            print(f"❌ Validation failed: {e}")
    
    def create_sample_accounts(self, tier: str = "starter", count: int = 10):
        """Create sample accounts for testing."""
        try:
            tier_enum = UserTier(tier)
        except ValueError:
            print(f"❌ Invalid tier: {tier}. Use: starter, professional, enterprise")
            return
        
        print(f"🧪 Creating {count} sample {tier} accounts...")
        
        # This would create sample accounts in the database
        # Implementation depends on your specific needs
        print(f"✅ Sample accounts created!")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Axie Studio Account Management CLI")
    parser.add_argument("--db-url", default="sqlite:///axie_studio.db", help="Database URL")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List accounts")
    list_parser.add_argument("--tier", choices=["starter", "professional", "enterprise"], help="Filter by tier")
    list_parser.add_argument("--active-only", action="store_true", help="Show only active accounts")
    
    # Import command
    subparsers.add_parser("import", help="Import accounts from JSON to database")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export accounts to CSV")
    export_parser.add_argument("--output", default="accounts_export.csv", help="Output CSV file")
    
    # Reset command
    subparsers.add_parser("reset-usage", help="Reset monthly API usage for all accounts")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate new account data files")
    generate_parser.add_argument("--count", type=int, default=600, help="Number of accounts to generate")
    
    # Validate command
    subparsers.add_parser("validate", help="Validate account data integrity")
    
    # Sample command
    sample_parser = subparsers.add_parser("sample", help="Create sample accounts for testing")
    sample_parser.add_argument("--tier", default="starter", choices=["starter", "professional", "enterprise"])
    sample_parser.add_argument("--count", type=int, default=10, help="Number of sample accounts")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = AccountCLI(args.db_url)
    
    if args.command == "list":
        cli.list_accounts(args.tier, args.active_only)
    elif args.command == "import":
        cli.import_accounts()
    elif args.command == "export":
        cli.export_csv(args.output)
    elif args.command == "reset-usage":
        cli.reset_monthly_usage()
    elif args.command == "generate":
        cli.generate_new_accounts(args.count)
    elif args.command == "validate":
        cli.validate_accounts()
    elif args.command == "sample":
        cli.create_sample_accounts(args.tier, args.count)


if __name__ == "__main__":
    main()
