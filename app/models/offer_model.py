from typing import Optional
from sqlalchemy import SmallInteger, Column
from sqlmodel import Field, SQLModel # type: ignore

from models.base_model import TimestampModel, UUIDModel, OwerModel



# Id (PK)

# 0: Private
# 1: Available (Public all)
# 2: Processing
# 3: Deleted
# 4: InvestorsPublic
# CreatedBy
# CreateAt
# LastModifiedBy
# LastModifiedAt

class OfferBase(SQLModel):
   name: str = Field(max_length=255, nullable=False)
   campaign_id: int = Field(
      nullable=False,
      sa_column_kwargs={
         "unique": True
      }
   )
   project_name: str = Field(max_length=255, nullable=False)
   homepage_url: str = Field(max_length=255, nullable=False)
   project_description: str = Field(max_length=1000, nullable=False)
   cpc: int = Field(nullable=False)
   min_days: int = Field(nullable=False)
   min_budgets: int = Field(nullable=False)
   note: str = Field(max_length=400)
   status: int = Field(default=0, sa_column=Column(SmallInteger()))



class Offer(
   TimestampModel,
   OfferBase,
   UUIDModel,
   table=True
):
   __tablename__ = f"Offers"


class OfferRead(OfferBase, UUIDModel):
   ...


class OfferCreate(OfferBase):
   ...


class OfferPatch(OfferBase):
   project_name: Optional[str] = Field(max_length=255)
   homepage_url: Optional[str] = Field(max_length=255)
   project_description: Optional[str] = Field(max_length=1000)
   cpc: Optional[int] 
   min_days: Optional[int] 
   min_budgets: Optional[int]
   note: Optional[str] = Field(max_length=400)
   status: Optional[int] 