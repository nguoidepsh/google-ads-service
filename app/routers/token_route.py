from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from models.google_token_model import Token, TokenCreate
from controllers.token_controller import get_tokens_func, create_token_func, login_func

token_router = APIRouter()

@token_router.get("/auth", response_model=Token)
async def auth(token: Annotated[TokenCreate, Depends(create_token_func)]):
    if not token:
        raise HTTPException(status_code=500, detail="Some things went wrong, while creating token.")
    return token

@token_router.get("/get_tokens", response_model=list[Token])
def get_token(tokens: Annotated[list[Token], Depends(get_tokens_func)]):
    if not tokens:
        raise HTTPException(status_code=404, detail="Token not found")
    return tokens

@token_router.get("/login")
async def login(response: Annotated[None, Depends(login_func)]): 
    return response