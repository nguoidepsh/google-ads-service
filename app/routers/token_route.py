from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from models.google_token_model import Token, TokenCreate
from controllers.google_token_controller import get_tokens_func, create_token_func

token_router = APIRouter()

@token_router.post("/create-token/", response_model=Token)
def create_token(token: Annotated[TokenCreate, Depends(create_token_func)]):
    if not token:
        raise HTTPException(status_code=500, detail="Some things went wrong, while creating token.")
    return token

@token_router.get("/get_tokens", response_model=list[Token])
def get_token(token: Annotated[Token, Depends(get_tokens_func)]):
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    return token