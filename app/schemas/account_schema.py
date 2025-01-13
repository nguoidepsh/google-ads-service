from enum import Enum
from uuid import UUID

from pydantic import BaseModel
from schemas.base_schema import TimestampModel, UUIDModel
from sqlmodel import Field


class AccountStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    AVAILABLE = "available"


class AccountBase(BaseModel):
    """
    Accountbase model for Account.

    Attributes:
        email (int):
        access_Account (int):
        refresh_Account
        expires_at:
    """

    customer_id: str = Field(max_length=10, nullable=False, unique=True, regex=r"^\d+$")
    status: AccountStatus = Field(nullable=False)
    provider_id: UUID = Field(default=None, foreign_key="Providers.id")


class AccountCreate(AccountBase): ...


class Account(UUIDModel, TimestampModel):
    uuid: int


class AccountUpdate(BaseModel):
    uuid: int
