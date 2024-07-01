from typing import Optional
from sqlmodel import SQLModel, Field # type: ignore
from datetime import datetime



class StatBase(SQLModel):
    """
    Stat model for Token.

    Attributes:
        
        keyword
        device
        url
        hours

        date
        campaign_id
        adgroup_id
        device
        click
        impression
        cpc
        cost

    """

    date: datetime
    campaign_id: str
    ad_group_id: str
    device: str
    clicks: int
    impressions: int
    average_cpc: float
    cost_micros: int


class SearchTermStat(StatBase, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True)  # Primary key for token


class SearchTermCreate(StatBase):
    pass