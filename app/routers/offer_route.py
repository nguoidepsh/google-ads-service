from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi import status as http_status

from models.offer_model import OfferRead, OfferCreate
from controllers.offer_controller import create, get

offer_router = APIRouter()


@offer_router.post("/create", response_model=OfferRead, status_code=http_status.HTTP_201_CREATED)
def create(data: Annotated[OfferCreate, Depends(create)]):
    if not data:
        raise HTTPException(status_code=500, detail="Some things went wrong, while creating offer.")
    return data


@offer_router.get("/get", response_model=list[OfferRead])
def get_token(offers: Annotated[list[OfferRead], Depends(get)]):
    if not offers:
        raise HTTPException(status_code=404, detail="Offers not found")
    return offers