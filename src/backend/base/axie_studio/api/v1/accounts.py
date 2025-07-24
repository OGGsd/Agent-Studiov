"""
Admin Account Management API
Endpoints for managing pre-configured commercial accounts.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import and_, or_

from axie_studio.services.database.models.user.model import User, UserTier, UserUpdate, TIER_LIMITS
from axie_studio.services.deps import get_session
from axie_studio.services.auth.utils import get_current_active_superuser
from axie_studio.services.account_manager import AccountManager
from pydantic import BaseModel


router = APIRouter(prefix="/accounts", tags=["accounts"])


class AccountResponse(BaseModel):
    id: str
    username: str
    tier: UserTier
    account_number: Optional[int]
    is_active: bool
    api_calls_used_this_month: int
    storage_used_gb: float
    workflow_count: int
    created_at: str
    last_login_at: Optional[str]
    tier_limits: dict


class AccountUpdate(BaseModel):
    username: Optional[str] = None
    tier: Optional[UserTier] = None
    is_active: Optional[bool] = None
    api_calls_used_this_month: Optional[int] = None
    storage_used_gb: Optional[float] = None


class AccountStats(BaseModel):
    total_accounts: int
    active_accounts: int
    tiers: dict
    usage_summary: dict
    potential_monthly_revenue: int


@router.get("/", response_model=List[AccountResponse])
async def get_all_accounts(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser),
    tier: Optional[str] = Query(None, description="Filter by tier"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search by username or account number"),
    skip: int = Query(0, ge=0, description="Number of accounts to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of accounts to return")
):
    """Get all pre-configured accounts with optional filtering."""
    
    query = session.query(User)
    
    # Apply filters
    if tier:
        try:
            tier_enum = UserTier(tier)
            query = query.filter(User.tier == tier_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid tier: {tier}")
    
    if active is not None:
        query = query.filter(User.is_active == active)
    
    if search:
        query = query.filter(
            or_(
                User.username.ilike(f"%{search}%"),
                User.account_number.ilike(f"%{search}%") if search.isdigit() else False
            )
        )
    
    # Apply pagination
    users = query.offset(skip).limit(limit).all()
    
    # Convert to response format
    accounts = []
    for user in users:
        tier_limits = TIER_LIMITS[user.tier]
        accounts.append(AccountResponse(
            id=str(user.id),
            username=user.username,
            tier=user.tier,
            account_number=user.account_number,
            is_active=user.is_active,
            api_calls_used_this_month=user.api_calls_used_this_month,
            storage_used_gb=user.storage_used_gb,
            workflow_count=len(user.flows),
            created_at=user.create_at.isoformat(),
            last_login_at=user.last_login_at.isoformat() if user.last_login_at else None,
            tier_limits={
                "max_workflows": tier_limits.max_workflows,
                "max_api_calls_per_month": tier_limits.max_api_calls_per_month,
                "max_storage_gb": tier_limits.max_storage_gb,
                "support_level": tier_limits.support_level,
                "price_per_month": tier_limits.price_per_month
            }
        ))
    
    return accounts


@router.get("/stats", response_model=AccountStats)
async def get_account_stats(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get statistics about all accounts."""
    
    account_manager = AccountManager(session)
    stats = account_manager.get_account_statistics()
    
    # Calculate potential revenue
    potential_revenue = 0
    for tier_name, tier_data in stats["tiers"].items():
        tier_limits = TIER_LIMITS[UserTier(tier_name)]
        potential_revenue += tier_data["count"] * tier_limits.price_per_month
    
    return AccountStats(
        total_accounts=stats["total_accounts"],
        active_accounts=stats["active_accounts"],
        tiers=stats["tiers"],
        usage_summary=stats["usage_summary"],
        potential_monthly_revenue=potential_revenue
    )


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get a specific account by ID."""
    
    user = session.query(User).filter(User.id == account_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Account not found")
    
    tier_limits = TIER_LIMITS[user.tier]
    
    return AccountResponse(
        id=str(user.id),
        username=user.username,
        tier=user.tier,
        account_number=user.account_number,
        is_active=user.is_active,
        api_calls_used_this_month=user.api_calls_used_this_month,
        storage_used_gb=user.storage_used_gb,
        workflow_count=len(user.flows),
        created_at=user.create_at.isoformat(),
        last_login_at=user.last_login_at.isoformat() if user.last_login_at else None,
        tier_limits={
            "max_workflows": tier_limits.max_workflows,
            "max_api_calls_per_month": tier_limits.max_api_calls_per_month,
            "max_storage_gb": tier_limits.max_storage_gb,
            "support_level": tier_limits.support_level,
            "price_per_month": tier_limits.price_per_month
        }
    )


@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: str,
    account_update: AccountUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Update an account's details."""
    
    user = session.query(User).filter(User.id == account_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Update fields
    update_data = account_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    session.commit()
    session.refresh(user)
    
    # Return updated account
    tier_limits = TIER_LIMITS[user.tier]
    
    return AccountResponse(
        id=str(user.id),
        username=user.username,
        tier=user.tier,
        account_number=user.account_number,
        is_active=user.is_active,
        api_calls_used_this_month=user.api_calls_used_this_month,
        storage_used_gb=user.storage_used_gb,
        workflow_count=len(user.flows),
        created_at=user.create_at.isoformat(),
        last_login_at=user.last_login_at.isoformat() if user.last_login_at else None,
        tier_limits={
            "max_workflows": tier_limits.max_workflows,
            "max_api_calls_per_month": tier_limits.max_api_calls_per_month,
            "max_storage_gb": tier_limits.max_storage_gb,
            "support_level": tier_limits.support_level,
            "price_per_month": tier_limits.price_per_month
        }
    )


@router.delete("/{account_id}")
async def delete_account(
    account_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Delete an account (use with caution)."""
    
    user = session.query(User).filter(User.id == account_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Don't allow deleting admin accounts
    if user.is_superuser:
        raise HTTPException(status_code=403, detail="Cannot delete admin accounts")
    
    session.delete(user)
    session.commit()
    
    return {"message": "Account deleted successfully"}


@router.post("/import")
async def import_accounts(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Import pre-configured accounts from the accounts data file."""
    
    account_manager = AccountManager(session)
    result = account_manager.create_accounts_in_database()
    
    return {
        "message": "Accounts imported successfully",
        "created": result["created"],
        "skipped": result["skipped"],
        "total": result["total"]
    }


@router.post("/reset-monthly-usage")
async def reset_monthly_usage(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Reset API call usage for all accounts (run monthly)."""
    
    account_manager = AccountManager(session)
    reset_count = account_manager.reset_monthly_usage()
    
    return {
        "message": f"Monthly usage reset for {reset_count} accounts"
    }


@router.get("/export/csv")
async def export_accounts_csv(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Export all accounts to CSV format."""
    
    account_manager = AccountManager(session)
    
    # Create temporary file path
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_path = f.name
    
    try:
        exported_count = account_manager.export_accounts_csv(csv_path)
        
        # Read the CSV content
        with open(csv_path, 'r') as f:
            csv_content = f.read()
        
        return {
            "message": f"Exported {exported_count} accounts",
            "csv_content": csv_content
        }
    
    finally:
        # Clean up temporary file
        if os.path.exists(csv_path):
            os.unlink(csv_path)
