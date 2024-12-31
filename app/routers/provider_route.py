from typing import List

from controllers.provider_controller import get_all
from fastapi import APIRouter, Depends
from models.provider_model import Provider
from schemas.base_schema import MultipeResponseModel

router = APIRouter()


@router.get("")
async def list_provider(
    providers: List[Provider] = Depends(get_all),
) -> MultipeResponseModel:
    return MultipeResponseModel(data=providers)
