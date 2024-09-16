from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel

T = TypeVar("T")


class UUIDModel(BaseModel):
    id: UUID


class TimestampModel(BaseModel):
    created_at: datetime
    updated_at: datetime


class BaseResponseModel(BaseModel):
    code: int = 200
    status: str = "success"
    message: str = "Data retrieved successfully"


class SingleResponseModel(BaseResponseModel, Generic[T]):
    data: Optional[T] = None


class MultipeResponseModel(BaseResponseModel, Generic[T]):
    data: list[Optional[T]] = None
    count: Optional[int] = None

    def __init__(self, **data):
        super().__init__(**data)
        if isinstance(self.data, list):
            self.count = len(self.data)
        else:
            self.count = None
