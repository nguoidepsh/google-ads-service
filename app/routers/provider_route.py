from typing import List

from controllers.provider_controller import create_provider, delete_provider, get_all, get_provider_by_id, update_provider
from fastapi import APIRouter, Depends
from models.provider_model import Provider
from schemas.base_schema import BaseResponseModel, MultipeResponseModel, SingleResponseModel

router = APIRouter()


@router.get("")
async def list_provider(
    providers: List[Provider] = Depends(get_all),
) -> MultipeResponseModel:
    return MultipeResponseModel(data=providers)


@router.get("/{id}")
async def get_provider(
    provider: Provider = Depends(get_provider_by_id)
) -> SingleResponseModel[Provider]:
    """
    Get a provider by ID.
    """
    return SingleResponseModel(data=provider)


@router.post("")
async def create_provider_endpoint(
    provider: Provider = Depends(create_provider)
) -> SingleResponseModel[Provider]:
    """
    Create a new provider.
    """
    return SingleResponseModel(data=provider, message="Provider created successfully")


@router.put("")
async def update_provider_endpoint(
    provider: Provider = Depends(update_provider)
) -> SingleResponseModel[Provider]:
    """
    Update an existing provider.
    """
    return SingleResponseModel(data=provider, message="Provider updated successfully")


@router.delete("/{id}")
async def delete_provider_endpoint(
    id: str = Depends(delete_provider)
) -> BaseResponseModel:
    """
    Delete a provider by ID.
    """
    return BaseResponseModel(message="Provider deleted successfully")
