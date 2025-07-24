"""
Tier-based Limits Service
Enforces usage limits based on user tier (Starter, Professional, Enterprise).
"""

from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from axie_studio.services.database.models.user.model import User, TIER_LIMITS
from axie_studio.services.database.models.flow.model import Flow


class TierLimitsService:
    """Service to enforce tier-based limits for users."""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def check_workflow_limit(self, user: User) -> bool:
        """Check if user can create more workflows."""
        limits = TIER_LIMITS[user.tier]

        # Enterprise has unlimited workflows
        if limits.max_workflows == -1:
            return True

        # Use async SQLAlchemy syntax
        stmt = select(func.count(Flow.id)).where(Flow.user_id == user.id)
        result = await self.db.execute(stmt)
        current_workflows = result.scalar()
        return current_workflows < limits.max_workflows
    
    def check_api_call_limit(self, user: User, calls_to_add: int = 1) -> bool:
        """Check if user can make more API calls this month."""
        limits = TIER_LIMITS[user.tier]
        return (user.api_calls_used_this_month + calls_to_add) <= limits.max_api_calls_per_month
    
    def check_storage_limit(self, user: User, storage_to_add_gb: float = 0) -> bool:
        """Check if user can use more storage."""
        limits = TIER_LIMITS[user.tier]
        return (user.storage_used_gb + storage_to_add_gb) <= limits.max_storage_gb
    
    async def enforce_workflow_limit(self, user: User) -> None:
        """Enforce workflow creation limit."""
        if not await self.check_workflow_limit(user):
            limits = TIER_LIMITS[user.tier]
            raise HTTPException(
                status_code=403,
                detail=f"Workflow limit reached. Your {user.tier.value} plan allows {limits.max_workflows} workflows. Upgrade to create more."
            )
    
    def enforce_api_call_limit(self, user: User, calls_to_add: int = 1) -> None:
        """Enforce API call limit."""
        if not self.check_api_call_limit(user, calls_to_add):
            limits = TIER_LIMITS[user.tier]
            remaining = limits.max_api_calls_per_month - user.api_calls_used_this_month
            raise HTTPException(
                status_code=403,
                detail=f"API call limit reached. You have {remaining} calls remaining this month. Your {user.tier.value} plan allows {limits.max_api_calls_per_month:,} calls per month."
            )
    
    def enforce_storage_limit(self, user: User, storage_to_add_gb: float = 0) -> None:
        """Enforce storage limit."""
        if not self.check_storage_limit(user, storage_to_add_gb):
            limits = TIER_LIMITS[user.tier]
            remaining = limits.max_storage_gb - user.storage_used_gb
            raise HTTPException(
                status_code=403,
                detail=f"Storage limit reached. You have {remaining:.2f}GB remaining. Your {user.tier.value} plan allows {limits.max_storage_gb}GB storage."
            )
    
    async def increment_api_calls(self, user: User, count: int = 1) -> None:
        """Increment user's API call count after checking limits."""
        self.enforce_api_call_limit(user, count)
        user.api_calls_used_this_month += count
        await self.db.commit()

    async def update_storage_usage(self, user: User, new_usage_gb: float) -> None:
        """Update user's storage usage after checking limits."""
        storage_diff = new_usage_gb - user.storage_used_gb
        if storage_diff > 0:  # Only check if increasing storage
            self.enforce_storage_limit(user, storage_diff)

        user.storage_used_gb = new_usage_gb
        await self.db.commit()
    
    async def get_user_usage_summary(self, user: User) -> dict:
        """Get user's current usage and limits."""
        limits = TIER_LIMITS[user.tier]

        # Use async SQLAlchemy syntax
        stmt = select(func.count(Flow.id)).where(Flow.user_id == user.id)
        result = await self.db.execute(stmt)
        workflow_count = result.scalar()
        
        return {
            "tier": user.tier.value,
            "usage": {
                "workflows": {
                    "current": workflow_count,
                    "limit": limits.max_workflows,
                    "percentage": (workflow_count / limits.max_workflows * 100) if limits.max_workflows != -1 else 0
                },
                "api_calls": {
                    "current": user.api_calls_used_this_month,
                    "limit": limits.max_api_calls_per_month,
                    "percentage": (user.api_calls_used_this_month / limits.max_api_calls_per_month * 100)
                },
                "storage": {
                    "current_gb": user.storage_used_gb,
                    "limit_gb": limits.max_storage_gb,
                    "percentage": (user.storage_used_gb / limits.max_storage_gb * 100)
                }
            },
            "limits": {
                "max_workflows": limits.max_workflows,
                "max_api_calls_per_month": limits.max_api_calls_per_month,
                "max_storage_gb": limits.max_storage_gb,
                "support_level": limits.support_level,
                "price_per_month": limits.price_per_month
            }
        }


def get_tier_limits_service(db_session: Session) -> TierLimitsService:
    """Dependency to get TierLimitsService instance."""
    return TierLimitsService(db_session)


# Decorator for endpoints that consume API calls
def track_api_call(calls: int = 1):
    """Decorator to track API call usage."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract user and db session from kwargs
            current_user = kwargs.get('current_user')
            session = kwargs.get('session')
            
            if current_user and session:
                limits_service = TierLimitsService(session)
                limits_service.increment_api_calls(current_user, calls)
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# Middleware function to check limits before workflow operations
async def check_workflow_limits(user: User, db_session: Session):
    """Check workflow limits before creating new workflows."""
    limits_service = TierLimitsService(db_session)
    limits_service.enforce_workflow_limit(user)


# Middleware function to check limits before file operations
async def check_storage_limits(user: User, db_session: Session, file_size_gb: float):
    """Check storage limits before uploading files."""
    limits_service = TierLimitsService(db_session)
    limits_service.enforce_storage_limit(user, file_size_gb)


# Usage tracking functions
async def track_workflow_creation(user: User, db_session: AsyncSession):
    """Track workflow creation (no additional usage, just enforce limit)."""
    limits_service = TierLimitsService(db_session)
    await limits_service.enforce_workflow_limit(user)


async def track_file_upload(user: User, db_session: AsyncSession, file_size_gb: float):
    """Track file upload and update storage usage."""
    limits_service = TierLimitsService(db_session)
    new_usage = user.storage_used_gb + file_size_gb
    await limits_service.update_storage_usage(user, new_usage)


async def track_api_execution(user: User, db_session: AsyncSession, api_calls: int = 1):
    """Track API execution and increment usage."""
    limits_service = TierLimitsService(db_session)
    await limits_service.increment_api_calls(user, api_calls)


# Helper function to get user's current plan info
async def get_user_plan_info(user: User, db_session: AsyncSession) -> dict:
    """Get comprehensive plan information for a user."""
    limits_service = TierLimitsService(db_session)
    return await limits_service.get_user_usage_summary(user)
