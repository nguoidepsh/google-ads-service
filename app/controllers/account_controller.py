from typing import List
from schemas.account_schema import AccountCreate, AccountUpdate
from db.db_connector import DB_SESSION
from fastapi import Depends, Request
from models.account_model import Account
from sqlmodel import select
from starlette.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError


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


async def get_accounts(session: DB_SESSION):
    return session.exec(
        select(Account)
    ).all()


async def create_account(session: DB_SESSION, request: Request, account_data: AccountCreate):
    """
    Create a new account.
    """
    userinfo = request.state.auth_data
    account = Account(**account_data.model_dump(), uuid=userinfo["uuid"])
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


async def create_accounts(
    session: DB_SESSION,
    request: Request,
    accounts_data: List[AccountCreate]
) -> List[Account]:
    """
    Create multiple accounts.
    """
    userinfo = request.state.auth_data
    created_accounts = []
    failed_accounts = []
    for account_data in accounts_data:
        try:
            existing_account = session.query(Account).filter(
                Account.customer_id == account_data.customer_id).first()
            if existing_account:
                failed_accounts.append({
                    "account_data": account_data,
                    "error": f"Customer ID {account_data.customer_id} already exists."
                })
                continue

            account = Account(**account_data.model_dump(),
                              uuid=userinfo["uuid"])
            session.add(account)
            created_accounts.append(account)

        except Exception as e:
            session.rollback()
            failed_accounts.append({
                "account_data": account_data,
                "error": f"Error: {str(e)}"
            })
            continue
    session.commit()
    for account in created_accounts:
        session.refresh(account)
    return {
        "created_accounts": created_accounts,
        "failed_accounts": failed_accounts
    }


async def update_account(session: DB_SESSION, updates: AccountUpdate):
    """
    Update an existing account by id.
    """
    account = session.exec(select(Account).where(
        Account.id == updates.id)).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    update_data = updates.model_dump()

    for key, value in update_data.items():
        setattr(account, key, value)

    session.add(account)
    session.commit()
    session.refresh(account)
    return account


async def delete_account(session: DB_SESSION, id: str):
    """
    Delete an account by id.
    """
    account = session.exec(select(Account).where(Account.id == id)).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    session.delete(account)
    session.commit()
    return {"message": "Account deleted successfully"}
