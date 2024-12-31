from typing import List

from controllers.account_controller import get_accounts_by_uuid
from fastapi import APIRouter, Depends
from models.account_model import Account
from schemas.base_schema import MultipeResponseModel

router = APIRouter()


@router.get("")
async def list_accounts(
    accounts: List[Account] = Depends(get_accounts_by_uuid),
) -> MultipeResponseModel:
    return MultipeResponseModel(data=accounts)
