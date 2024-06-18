
from fastapi import HTTPException
from sqlmodel import select
from db.db_connector import DB_SESSION
from models.google_token_model import Token
# from sqlalchemy import or_


def get_tokens_func(session: DB_SESSION):
    tokens = session.exec(select(Token)).all()
    if tokens:
        return tokens
    raise HTTPException(status_code=404, detail="Tokens not found")


def create_token_func(
    token_details: Token,
    session: DB_SESSION,
):
    # Verify that token details are provided
    if not token_details:
        raise HTTPException(
            status_code=400, detail="Token not found!"
        )
    try:
        token = Token(user_id=token_details.user_id, access_token=token_details.access_token, refresh_token=token_details.refresh_token, expires_at=token_details.expires_at)
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