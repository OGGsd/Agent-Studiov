#!/usr/bin/env python3
"""
Database diagnostic script to run on DigitalOcean app
"""
import asyncio
import sys
from sqlalchemy import text

# Add the current directory to Python path
sys.path.append('.')

from axie_studio.services.deps import get_db_service

async def check_database():
    """Check database tables and content"""
    try:
        db_service = get_db_service()
        
        async with db_service.with_session() as session:
            print("🔍 DATABASE DIAGNOSTIC REPORT")
            print("=" * 50)
            
            # Check if tables exist
            print("\n📋 CHECKING TABLES:")
            tables_query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """
            result = await session.execute(text(tables_query))
            tables = result.fetchall()
            
            if tables:
                print(f"✅ Found {len(tables)} tables:")
                for table in tables:
                    print(f"   • {table[0]}")
            else:
                print("❌ No tables found!")
                return
            
            # Check user table specifically
            print("\n👤 CHECKING USER TABLE:")
            try:
                user_count_query = 'SELECT COUNT(*) FROM "user";'
                result = await session.execute(text(user_count_query))
                user_count = result.scalar()
                print(f"✅ User table exists with {user_count} users")
                
                if user_count > 0:
                    # Check user details
                    users_query = """
                        SELECT username, is_active, is_superuser, tier, account_number 
                        FROM "user" 
                        ORDER BY username 
                        LIMIT 10;
                    """
                    result = await session.execute(text(users_query))
                    users = result.fetchall()
                    print(f"📊 First 10 users:")
                    for user in users:
                        print(f"   • {user[0]} (active: {user[1]}, super: {user[2]}, tier: {user[3]}, account: {user[4]})")
                
                # Check for admin user specifically
                admin_query = """
                    SELECT username, is_active, is_superuser 
                    FROM "user" 
                    WHERE username = 'stefan@axiestudio.se';
                """
                result = await session.execute(text(admin_query))
                admin = result.fetchone()
                if admin:
                    print(f"✅ Admin user found: {admin[0]} (active: {admin[1]}, super: {admin[2]})")
                else:
                    print("❌ Admin user NOT found!")
                    
            except Exception as e:
                print(f"❌ Error checking user table: {e}")
            
            # Check alembic version
            print("\n🔄 CHECKING MIGRATION STATUS:")
            try:
                version_query = "SELECT version_num FROM alembic_version;"
                result = await session.execute(text(version_query))
                version = result.scalar()
                print(f"✅ Current migration version: {version}")
            except Exception as e:
                print(f"❌ Error checking migration version: {e}")
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_database())
