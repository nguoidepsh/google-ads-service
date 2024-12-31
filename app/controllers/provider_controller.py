from db.db_connector import DB_SESSION
from fastapi import Depends, Request
from models.provider_model import Provider
from sqlmodel import select
from starlette.exceptions import HTTPException


async def get_all(session: DB_SESSION):
    return session.exec(select(Provider)).all()
