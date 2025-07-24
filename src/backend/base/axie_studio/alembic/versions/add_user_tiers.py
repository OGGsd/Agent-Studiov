"""Add user tiers and commercial features

Revision ID: add_user_tiers
Revises: 
Create Date: 2025-07-24 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_user_tiers'
down_revision = None  # Will be updated to latest revision
head = None


def upgrade():
    """Add tier-related columns to user table."""
    # Add enum type for user tiers
    tier_enum = postgresql.ENUM('starter', 'professional', 'enterprise', name='usertier')
    tier_enum.create(op.get_bind())
    
    # Add new columns to user table
    op.add_column('user', sa.Column('tier', tier_enum, nullable=False, server_default='starter'))
    op.add_column('user', sa.Column('api_calls_used_this_month', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('user', sa.Column('storage_used_gb', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('user', sa.Column('account_number', sa.Integer(), nullable=True))
    
    # Create index on account_number for faster lookups
    op.create_index('ix_user_account_number', 'user', ['account_number'])
    op.create_index('ix_user_tier', 'user', ['tier'])


def downgrade():
    """Remove tier-related columns from user table."""
    # Drop indexes
    op.drop_index('ix_user_tier', table_name='user')
    op.drop_index('ix_user_account_number', table_name='user')
    
    # Drop columns
    op.drop_column('user', 'account_number')
    op.drop_column('user', 'storage_used_gb')
    op.drop_column('user', 'api_calls_used_this_month')
    op.drop_column('user', 'tier')
    
    # Drop enum type
    tier_enum = postgresql.ENUM('starter', 'professional', 'enterprise', name='usertier')
    tier_enum.drop(op.get_bind())
