from db.db_connector import DB_SESSION
from fastapi import Depends, Request
from models.account_model import Account
from sqlmodel import select
from starlette.exceptions import HTTPException


async def get_accounts_by_uuid(session: DB_SESSION, request: Request):
    userinfo = request.state.auth_data
    return session.exec(
        select(Account).where(Account.uuid == int(userinfo["uuid"]))
    ).all()


async def get_account_by_customer_id(session: DB_SESSION, customer_id: str):
    return session.exec(
        select(Account).where(Account.customer_id == customer_id)
    ).first()


async def valid_owner(
    request: Request, account: Account = Depends(get_account_by_customer_id)
):
    userinfo = request.state.auth_data
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.uuid != int(userinfo["uuid"]):
        raise HTTPException(status_code=403, detail="Permission denied")

    return account
