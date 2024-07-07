# Ticket_id
# TaskTypeId
# Values
# Status
# 0: Pending
# 1: Completed
# 2: Processing
# 3: Error

from models.ticket_model import Ticket
from sqlalchemy.dialects import postgresql
from sqlalchemy import Column, event
from sqlmodel import Field, SQLModel, Relationship
import uuid as uuid_pkg
from models.base_model import TimestampModel, UUIDModel


task_type = postgresql.ENUM(
   "cpc",
   "ref",
   "keyword",
   "computer",
   "tablet",
   "mobile",
   "location",
   "excluded",
   name=f"task_type"
)

@event.listens_for(SQLModel.metadata, "before_create")
def _create_enums(metadata, conn, **kw):  # noqa: indirect usage
   task_type.create(conn, checkfirst=True)


class TaskBase(SQLModel):
   ticket_id : uuid_pkg.UUID = Field(nullable=False, foreign_key="Tickets.id")
   task_type : str = Field(sa_column=Column("task_type", task_type, nullable=True))
   values: str = Field(max_length=255, nullable=False)
   
   # status: int = Field(default=0, sa_column=Column(SmallInteger()))



class Task(TimestampModel, TaskBase, UUIDModel, table=True):
    __tablename__ = f"Tasks"
    ticket: Ticket = Relationship(back_populates="tasks")
    



class TaskRead(TaskBase, UUIDModel):
   ...


class TaskCreate(TaskBase):
   ...


class TaskPatch(TaskBase):
    ...