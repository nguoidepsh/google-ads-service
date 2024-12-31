from enum import Enum

from pydantic import BaseModel
from schemas.base_schema import TimestampModel, UUIDModel
from sqlmodel import Field


class ProviderType(str, Enum):
    PROMO = "promo"
    INVOICE = "invoice"
    DISCOUNT = "discount"


class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ProviderBase(BaseModel):
    email: str = Field(nullable=False, foreign_key="Emails.email")

    name: str = Field(max_length=255, nullable=False)
    description: str = Field(max_length=255, nullable=False)
    rate: float = Field(nullable=False)
    spreadsheet_id: str = Field(max_length=255, nullable=True)
    login_customer_id: str = Field(max_length=255, nullable=False)
    currency: str = Field(max_length=255, nullable=False)
    status: Status = Field(nullable=False, default="active")
    type: ProviderType = Field(nullable=False)


class ProviderCreate(ProviderBase): ...


class Provider(ProviderBase, UUIDModel, TimestampModel): ...
