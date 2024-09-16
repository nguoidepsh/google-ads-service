from typing import Annotated

from controllers.email_controller import (
    create_email,
    get_email_by_uuid,
    get_tokens_func,
    login_func,
)
from fastapi import APIRouter, Depends, HTTPException
from schemas.email_schema import Email, EmailCreate

email_router = APIRouter()


@email_router.get("/auth", response_model=Email)
async def auth(token: Annotated[EmailCreate, Depends(create_email)]):
    if not token:
        raise HTTPException(
            status_code=500, detail="Some things went wrong, while creating token."
        )
    return token


@email_router.get("/get_emails", response_model=list[Email])
def get_token(tokens: Annotated[list[Email], Depends(get_email_by_uuid)]):
    if not tokens:
        raise HTTPException(status_code=404, detail="Token not found")
    return tokens


@email_router.get("/login")
async def login(response: Annotated[None, Depends(login_func)]):
    return response
