from typing import Optional
import uuid as uuid_pkg

from sqlalchemy import SmallInteger, Column
from sqlmodel import Field, SQLModel # type: ignore

from models.base_model import TimestampModel, UUIDModel


# Id
# Name
# RefLink
# Cpc
# Countries (JSON)
# {'Vietnam':1, 'UnitedStates':1,}
# Từ khóa (JSON)
# {'Jasper':1, 'the best market':0,}
# Thiết bị (JSON)
# {'Desktop':80, 'mobile':-100,'tablet':-50,}
# OfferId
# Status
# 1: Available
# 2: Accept
# 3: Deny


class TicketBase(SQLModel):
   name: str = Field(max_length=255, nullable=False)
   offer_id: uuid_pkg.UUID
   status: int = Field(default=0, sa_column=Column(SmallInteger()))


1
class Ticket(
   TimestampModel,
   TicketBase,
   UUIDModel,
   table=True
):
   __tablename__ = f"Tickets"


class TicketRead(TicketBase, UUIDModel):
   ...


class TicketCreate(TicketBase):
   ...


class TicketPatch(TicketBase):
    ...