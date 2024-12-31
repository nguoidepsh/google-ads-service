from pydantic import BaseModel
from sqlmodel import Field

from schemas.base_schema import TimestampModel, UUIDModel


class EmailBase(BaseModel):
    """
    Emailbase model for Email.

    Attributes:
        email (int):
        access_Email (int):
        refresh_Email
        expires_at:
    """

    email: str = Field(max_length=255, nullable=False)
    access_token: str = Field(max_length=255, nullable=False)
    refresh_token: str = Field(max_length=255, nullable=False)
    expires_at: int = Field(nullable=False)


class EmailCreate(EmailBase): ...


class Email(EmailBase, UUIDModel, TimestampModel):
    uuid: int
