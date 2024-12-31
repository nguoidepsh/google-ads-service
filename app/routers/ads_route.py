from typing import Annotated

from controllers.ads_controller import (
    deposit,
    get_data,
    list_accounts,
    list_campaigns,
    list_child_accounts,
    set_tracking,
)
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from schemas.base_schema import MultipeResponseModel, SingleResponseModel

ads_router = APIRouter()


@ads_router.get("/list_accounts")
async def list_accounts(response=Depends(list_accounts)):
    return response


@ads_router.get("/list_child_accounts")
async def list_child_accounts(response=Depends(list_child_accounts)):
    return response


@ads_router.get("/list_campaigns")
async def list_campaigns(response=Depends(list_campaigns)):
    return response


@ads_router.post("/set_tracking", response_model=SingleResponseModel)
async def set_tracking(response=Depends(set_tracking)):
    return SingleResponseModel(
        status="success", message="Tracking set successfully", data=response
    )


# # get all adss
# @ads_router.get("/", response_model=list[Ticket])
# async def get_all_adss():
#     return get()


@ads_router.post("/deposit", response_model=SingleResponseModel)
async def deposit(response=Depends(deposit)):
    return SingleResponseModel(
        status="success", message="Deposit successful", data=response
    )
