"""Add user tiers and commercial features

Revision ID: add_user_tiers
Revises: 3162e83e485f
Create Date: 2025-07-24 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_user_tiers'
down_revision = '3162e83e485f'  # Points to the latest Langflow migration
head = None


def upgrade():
    """Add tier-related columns to user table."""
    # Check if columns exist before adding them
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('user')]

    # Add enum type for user tiers if it doesn't exist
    if 'tier' not in columns:
        tier_enum = postgresql.ENUM('starter', 'professional', 'enterprise', name='usertier')
        tier_enum.create(op.get_bind())

        # Add new columns to user table
        op.add_column('user', sa.Column('tier', tier_enum, nullable=False, server_default='starter'))

    if 'api_calls_used_this_month' not in columns:
        op.add_column('user', sa.Column('api_calls_used_this_month', sa.Integer(), nullable=False, server_default='0'))
    if 'storage_used_gb' not in columns:
        op.add_column('user', sa.Column('storage_used_gb', sa.Float(), nullable=False, server_default='0.0'))
    if 'account_number' not in columns:
        op.add_column('user', sa.Column('account_number', sa.Integer(), nullable=True))

    # Create indexes if they don't exist
    try:
        op.create_index('ix_user_account_number', 'user', ['account_number'])
    except:
        pass  # Index already exists
    try:
        op.create_index('ix_user_tier', 'user', ['tier'])
    except:
        pass  # Index already exists


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
