from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4
from enum import Enum

from pydantic import BaseModel
from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

from axie_studio.schema.serialize import UUIDstr

if TYPE_CHECKING:
    from axie_studio.services.database.models.api_key.model import ApiKey
    from axie_studio.services.database.models.flow.model import Flow
    from axie_studio.services.database.models.folder.model import Folder
    from axie_studio.services.database.models.variable.model import Variable


class UserTier(str, Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class TierLimits(BaseModel):
    max_workflows: int
    max_api_calls_per_month: int
    max_storage_gb: int
    support_level: str
    price_per_month: int


class UserOptin(BaseModel):
    github_starred: bool = Field(default=False)
    dialog_dismissed: bool = Field(default=False)
    discord_clicked: bool = Field(default=False)
    # Add more opt-in actions as needed


class User(SQLModel, table=True):  # type: ignore[call-arg]
    id: UUIDstr = Field(default_factory=uuid4, primary_key=True, unique=True)
    username: str = Field(index=True, unique=True)
    password: str = Field()
    profile_image: str | None = Field(default=None, nullable=True)
    is_active: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login_at: datetime | None = Field(default=None, nullable=True)

    # Commercial tier system
    tier: UserTier = Field(default=UserTier.STARTER)
    api_calls_used_this_month: int = Field(default=0)
    storage_used_gb: float = Field(default=0.0)
    account_number: int | None = Field(default=None, nullable=True)  # For pre-configured accounts
    api_keys: list["ApiKey"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    store_api_key: str | None = Field(default=None, nullable=True)
    flows: list["Flow"] = Relationship(back_populates="user")
    variables: list["Variable"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    folders: list["Folder"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "delete"},
    )
    optins: dict[str, Any] | None = Field(
        sa_column=Column(JSON, default=lambda: UserOptin().model_dump(), nullable=True)
    )


class UserCreate(SQLModel):
    username: str = Field()
    password: str = Field()
    tier: UserTier = Field(default=UserTier.STARTER)
    account_number: int | None = Field(default=None, nullable=True)
    optins: dict[str, Any] | None = Field(
        default={"github_starred": False, "dialog_dismissed": False, "discord_clicked": False}
    )


class UserRead(SQLModel):
    id: UUID = Field(default_factory=uuid4)
    username: str = Field()
    profile_image: str | None = Field()
    store_api_key: str | None = Field(nullable=True)
    is_active: bool = Field()
    is_superuser: bool = Field()
    create_at: datetime = Field()
    updated_at: datetime = Field()
    last_login_at: datetime | None = Field(nullable=True)
    tier: UserTier = Field()
    api_calls_used_this_month: int = Field()
    storage_used_gb: float = Field()
    account_number: int | None = Field(nullable=True)
    optins: dict[str, Any] | None = Field(default=None)


class UserUpdate(SQLModel):
    username: str | None = None
    profile_image: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    last_login_at: datetime | None = None
    tier: UserTier | None = None
    api_calls_used_this_month: int | None = None
    storage_used_gb: float | None = None
    account_number: int | None = None
    optins: dict[str, Any] | None = None


# Tier configuration constants
TIER_LIMITS = {
    UserTier.STARTER: TierLimits(
        max_workflows=50,
        max_api_calls_per_month=5000,
        max_storage_gb=1,
        support_level="Email",
        price_per_month=29
    ),
    UserTier.PROFESSIONAL: TierLimits(
        max_workflows=200,
        max_api_calls_per_month=25000,
        max_storage_gb=10,
        support_level="Priority",
        price_per_month=79
    ),
    UserTier.ENTERPRISE: TierLimits(
        max_workflows=-1,  # Unlimited
        max_api_calls_per_month=100000,
        max_storage_gb=50,
        support_level="24/7",
        price_per_month=199
    )
}
