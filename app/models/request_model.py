from models.base_model import TimestampModel, UUIDModel
from schemas.request_chema import RequestBase
from sqlmodel import Field, Relationship  # type: ignore


class Request(TimestampModel, RequestBase, UUIDModel, table=True):
    __tablename__ = f"Requests"
    uuid: int = Field(nullable=False)

    # relationships
    account: "Account" = Relationship(back_populates="requests")
