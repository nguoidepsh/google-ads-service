from typing import List

from controllers.requests_controller import (
    approve_request,
    create_request,
    get_requests,
    get_requests_by_uuid,
)
from fastapi import APIRouter, Depends, HTTPException
from models.request_model import Request
from schemas.base_schema import MultipeResponseModel

router = APIRouter()


@router.post("")
async def create_request(response=Depends(create_request)):
    if not response:
        raise HTTPException(status_code=500, detail="Some things went wrong.")
    return response


@router.put("/{request_id}/approve")
async def approve_request(response=Depends(approve_request)):
    if not response:
        raise HTTPException(status_code=500, detail="Some things went wrong.")
    return response


@router.get("")
async def list_requests(
    requests: List[Request] = Depends(get_requests),
) -> MultipeResponseModel:
    return MultipeResponseModel(data=requests)
