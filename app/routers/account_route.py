from typing import List
from fastapi import APIRouter, Body, Depends
from db.db_connector import DB_SESSION
from schemas.account_schema import AccountCreate, AccountUpdate
from controllers.account_controller import (
    get_accounts_by_uuid,
    get_accounts,
    create_account,
    update_account,
    delete_account,
)
from models.account_model import Account
from schemas.base_schema import BaseResponseModel, MultipeResponseModel, SingleResponseModel

router = APIRouter()

@router.get("")
async def list_accounts_by_uuid(
    accounts: List[Account] = Depends(get_accounts_by_uuid),
) -> MultipeResponseModel:
    return MultipeResponseModel(data=accounts)

@router.get("/all")
async def list_accounts(
    accounts: List[Account] = Depends(get_accounts),
) -> MultipeResponseModel:
    return MultipeResponseModel(data=accounts)

@router.post("")
async def create_account_endpoint(
    account: AccountCreate = Depends(create_account)
) -> SingleResponseModel[Account]:
    return SingleResponseModel(data=account, message="Account created successfully")

@router.put("")
async def update_account_endpoint(
    account: AccountUpdate = Depends(update_account)
) -> SingleResponseModel[Account]:    
    return SingleResponseModel(data=account, message="Account updated successfully")

@router.delete("/{id}")
async def delete_account_endpoint(
    id: str = Depends(delete_account)
) -> BaseResponseModel:
    return BaseResponseModel(message="Account deleted successfully")
