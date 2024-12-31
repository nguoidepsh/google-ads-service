from models.base_model import OwerModel, TimestampModel, UUIDModel
from schemas.email_schema import EmailBase
from sqlmodel import Field, Relationship, SQLModel  # type: ignore


class Email(TimestampModel, EmailBase, UUIDModel, table=True):
    __tablename__ = f"Emails"
    uuid: int = Field(nullable=False)

    # relationships
    providers: list["Provider"] = Relationship(back_populates="email_relationship")
