from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi import status as http_status

from models.stat_model import SearchTermStat, SearchTermCreate
from controllers.stat_controller import create

stat_router = APIRouter()


@stat_router.post("/create", response_model=SearchTermStat, status_code=http_status.HTTP_201_CREATED)
def create(stat: Annotated[SearchTermStat, Depends(create)]):
    if not stat:
        raise HTTPException(status_code=500, detail="Some things went wrong, while creating token.")
    return stat