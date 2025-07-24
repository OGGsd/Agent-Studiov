"""
User Profile API
Endpoints for user profile management and tier information.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel

from axie_studio.services.database.models.user.model import User, UserUpdate
from axie_studio.services.deps import get_session
from axie_studio.services.auth.utils import get_current_active_user, get_password_hash
from axie_studio.services.tier_limits import get_user_plan_info


router = APIRouter(prefix="/profile", tags=["profile"])


class ProfileResponse(BaseModel):
    id: str
    username: str
    tier: str
    account_number: int | None
    is_active: bool
    created_at: str
    last_login_at: str | None
    plan_info: dict


class ProfileUpdate(BaseModel):
    username: str | None = None
    password: str | None = None


@router.get("/", response_model=ProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """Get current user's profile and plan information."""

    plan_info = await get_user_plan_info(current_user, session)

    return ProfileResponse(
        id=str(current_user.id),
        username=current_user.username,
        tier=current_user.tier.value,
        account_number=current_user.account_number,
        is_active=current_user.is_active,
        created_at=current_user.create_at.isoformat(),
        last_login_at=current_user.last_login_at.isoformat() if current_user.last_login_at else None,
        plan_info=plan_info
    )


@router.put("/", response_model=ProfileResponse)
async def update_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """Update current user's profile (username and password only)."""
    
    update_data = profile_update.model_dump(exclude_unset=True)
    
    # Hash password if provided
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    
    # Check if username is already taken
    if "username" in update_data:
        existing_user = session.query(User).filter(
            User.username == update_data["username"],
            User.id != current_user.id
        ).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    # Update user
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    session.commit()
    session.refresh(current_user)
    
    # Return updated profile
    plan_info = await get_user_plan_info(current_user, session)

    return ProfileResponse(
        id=str(current_user.id),
        username=current_user.username,
        tier=current_user.tier.value,
        account_number=current_user.account_number,
        is_active=current_user.is_active,
        created_at=current_user.create_at.isoformat(),
        last_login_at=current_user.last_login_at.isoformat() if current_user.last_login_at else None,
        plan_info=plan_info
    )


@router.get("/usage")
async def get_usage_summary(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """Get detailed usage summary for the current user."""

    return await get_user_plan_info(current_user, session)


@router.get("/plan")
async def get_plan_details(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """Get plan details and limits for the current user."""

    plan_info = await get_user_plan_info(current_user, session)

    return {
        "tier": current_user.tier.value,
        "account_number": current_user.account_number,
        "limits": plan_info["limits"],
        "usage": plan_info["usage"]
    }
