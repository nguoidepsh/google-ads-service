import uuid as uuid_pkg
from typing import List


from sqlalchemy import SmallInteger, Column
from sqlmodel import Field, SQLModel, Relationship
from models.base_model import TimestampModel, UUIDModel


class TicketBase(SQLModel):
   name: str = Field(max_length=255, nullable=False)
   offer_id: uuid_pkg.UUID = Field(nullable=False, foreign_key="Offers.id")
   status: int = Field(default=0, sa_column=Column(SmallInteger()))


class Ticket(TimestampModel, TicketBase, UUIDModel, table=True):
   __tablename__ = f"Tickets"

   tasks: list["Task"] = Relationship(back_populates="ticket")



class TicketRead(TicketBase, UUIDModel):
   ...


class TicketCreate(TicketBase):
   tasks: List["TaskCreate"]



class TicketPatch(TicketBase):
    ...


