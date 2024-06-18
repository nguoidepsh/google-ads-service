from starlette.requests import Request

from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from models.google_token_model import Token, TokenCreate
from controllers.oauth_controller import oauth

oauth_router = APIRouter()

@oauth_router.get("/login")
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)

@oauth_router.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except:
        raise HTTPException(status_code=500, detail="Some things went wrong, while creating token.")
    return token
