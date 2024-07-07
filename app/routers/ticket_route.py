from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi import status as http_status

from models.ticket_model import TicketRead, TicketCreate
from controllers.ticket_controller import create, get

ticket_route = APIRouter()


@ticket_route.post("/create", response_model=TicketRead, status_code=http_status.HTTP_201_CREATED)
def create(data: Annotated[TicketCreate, Depends(create)]):
    if not data:
        raise HTTPException(status_code=500, detail="Some things went wrong, while creating offer.")
    return data


@ticket_route.get("/get", response_model=list[TicketRead])
def get_token(offers: Annotated[list[TicketRead], Depends(get)]):
    if not offers:
        raise HTTPException(status_code=404, detail="Offers not found")
    return offers