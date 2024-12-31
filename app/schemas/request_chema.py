from enum import Enum
from uuid import UUID

from pydantic import BaseModel
from schemas.base_schema import TimestampModel, UUIDModel
from sqlmodel import Field


class RequestStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class RequestType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    ACCOUNT = "ACCOUNT"


class RequestBase(BaseModel):
    account_id: str = Field(nullable=True, foreign_key="Accounts.customer_id")
    type: RequestType = Field(nullable=False)
    status: RequestStatus = Field(nullable=False, default="PENDING")
    amount: float = Field(nullable=False)
    reason: str = Field(max_length=255, nullable=True)


class RequestCreate(BaseModel):
    account_id: str | None = None
    type: RequestType
    amount: float


class Request(RequestBase, UUIDModel, TimestampModel): ...
