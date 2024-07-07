import uuid as uuid_pkg
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import text# type: ignore
from sqlmodel import Field, SQLModel# type: ignore


# class HealthCheck(BaseModel):
#    name: str
#    version: str
#    description: str


class UUIDModel(SQLModel):
   id: uuid_pkg.UUID = Field(
       default_factory=uuid_pkg.uuid4,
       primary_key=True,
       index=True,
       nullable=False,
       sa_column_kwargs={
           "server_default": text("gen_random_uuid()"),
           "unique": True
       }
   )


class TimestampModel(SQLModel):
   created_at: datetime = Field(
       default_factory=datetime.utcnow,
       nullable=False,
       sa_column_kwargs={
           "server_default": text("current_timestamp(0)")
       }
   )

   updated_at: datetime = Field(
       default_factory=datetime.utcnow,
       nullable=False,
       sa_column_kwargs={
           "server_default": text("current_timestamp(0)"),
           "onupdate": text("current_timestamp(0)")
       }
   )

class OwerModel(SQLModel):
    created_by: uuid_pkg.UUID = Field(
        nullable=False
    )

    updated_by: uuid_pkg.UUID = Field(
       nullable=False
   )