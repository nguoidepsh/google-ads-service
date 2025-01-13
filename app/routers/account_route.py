from pprint import pprint
from typing import List

from controllers.account_controller import (
    create_account,
    create_accounts,
    delete_account,
    get_accounts,
    get_accounts_by_uuid,
    update_account,
)
from db.db_connector import DB_SESSION
from fastapi import APIRouter, Body, Depends, Request
from models.account_model import Account
from schemas.account_schema import AccountCreate, AccountUpdate
from schemas.base_schema import (
    BaseResponseModel,
    MultipeResponseModel,
    SingleResponseModel,
)

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
    account: AccountCreate = Depends(create_account),
) -> SingleResponseModel[Account]:
    return SingleResponseModel(data=account, message="Account created successfully")


@router.post("/bulk")
async def create_accounts_endpoint(
    accounts_data: List[AccountCreate] = Depends(create_accounts),
) -> MultipeResponseModel:
    """
    Create multiple accounts.
    """
    created_accounts = accounts_data.get("created_accounts", [])
    failed_accounts = accounts_data.get("failed_accounts", [])

    pprint({"created": created_accounts, "failed": failed_accounts}, indent=2)
    return MultipeResponseModel(
        data=[{"created": created_accounts}, {"failed": failed_accounts}]
    )


@router.put("")
async def update_account_endpoint(
    account: AccountUpdate = Depends(update_account),
) -> SingleResponseModel[Account]:
    return SingleResponseModel(data=account, message="Account updated successfully")


@router.delete("/{id}")
async def delete_account_endpoint(
    id: str = Depends(delete_account),
) -> BaseResponseModel:
    return BaseResponseModel(message="Account deleted successfully")
