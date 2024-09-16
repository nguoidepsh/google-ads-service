from db.db_connector import DB_SESSION
from fastapi import HTTPException, Request
from models.email_model import Email
from settings import OAUTH
from sqlmodel import select  # type: ignore


def get_tokens_func(session: DB_SESSION):
    return session.exec(select(Email)).all()


def get_email_by_mail(session: DB_SESSION, email: str):
    return session.exec(select(Email).where(Email.email == email)).first()


async def login_func(request: Request):
    return await OAUTH.google.authorize_redirect(request, "https://dev.nguoidepsh.com/auth")  # type: ignore


async def create_email(request: Request, session: DB_SESSION):
    email_details = await OAUTH.google.authorize_access_token(request)  # type: ignore
    userinfo = request.state.auth_data

    email = Email(
        
        uuid=userinfo["uuid"],
        email=email_details["userinfo"].email,
        access_token=email_details["access_token"],
        refresh_token=email_details["refresh_token"],
        expires_at=email_details["expires_at"],
    )
    # Add the Email instance to the session and commit the transaction
    session.add(email)
    session.commit()
    session.refresh(email)
    return email


async def get_email_by_uuid(request: Request, session: DB_SESSION):
    userinfo = request.state.auth_data
    print(userinfo)
    return session.exec(select(Email).where(Email.uuid == int(userinfo["uuid"]))).all()
