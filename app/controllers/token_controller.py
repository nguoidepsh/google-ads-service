
from fastapi import HTTPException
from sqlmodel import select # type: ignore
from db.db_connector import DB_SESSION
from models.google_token_model import Token
from authlib.integrations.starlette_client import OAuth # type: ignore
from settings import CLIENT_ID, CLIENT_SECRET
from starlette.requests import Request
# from sqlalchemy import or_

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_params={'access_type': 'offline', 'prompt': 'consent' },
    client_kwargs={
        'scope': 'email openid profile https://www.googleapis.com/auth/adwords'}
)

def get_tokens_func(session: DB_SESSION):
    tokens = session.exec(select(Token)).all()
    if tokens:
        return tokens
    raise HTTPException(status_code=404, detail="Tokens not found")

async def login_func(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)

async def create_token_func(request: Request, session: DB_SESSION):
    # Verify that token details are provided
    try:
        token_details = await oauth.google.authorize_access_token(request)
        token = Token(email=token_details['userinfo'].email, access_token=token_details['access_token'], refresh_token=token_details['refresh_token'], expires_at=token_details['expires_at'])
        # Add the Token instance to the session and commit the transaction
        session.add(token)
        session.commit()
        session.refresh(token)
        return token

    except Exception as e:
        print("Error while creating Token:", e)
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the token."
        )