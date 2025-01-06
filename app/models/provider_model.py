from models.base_model import TimestampModel, UUIDModel
from schemas.provider_schema import ProviderBase
from sqlmodel import Field, Relationship  # type: ignore


class Provider(TimestampModel, ProviderBase, UUIDModel, table=True):
    __tablename__ = f"Providers"

    # relationships
    accounts: list["Account"] = Relationship(back_populates="provider")
    email_relationship: "Email" = Relationship(back_populates="providers")


class ProviderCreate(ProviderBase):
    pass


class ProviderUpdate(ProviderBase):
    id: str
