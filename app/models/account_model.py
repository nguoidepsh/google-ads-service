from models.base_model import TimestampModel, UUIDModel
from schemas.account_schema import AccountBase
from sqlmodel import Field, Relationship  # type: ignore


class Account(TimestampModel, AccountBase, UUIDModel, table=True):
    __tablename__ = f"Accounts"
    uuid: int = Field(nullable=False)

    # relationships
    provider: "Provider" = Relationship(back_populates="accounts")
    requests: list["Request"] = Relationship(back_populates="account")
