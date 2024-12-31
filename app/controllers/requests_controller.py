import uuid

from controllers.account_controller import get_account_by_customer_id
from db.db_connector import DB_SESSION
from fastapi import HTTPException
from fastapi import Request as FastAPIRequest
from models.account_model import Account
from models.provider_model import Provider
from models.request_model import Request
from schemas.request_chema import RequestCreate, RequestStatus
from sqlmodel import select


async def create_request(db: DB_SESSION, request: FastAPIRequest, data: RequestCreate):
    userinfo = request.state.auth_data

    db_request = Request(
        uuid=int(userinfo["uuid"]),
        account_id=data.account_id,
        type=data.type,
        amount=data.amount,
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


async def approve_request(db: DB_SESSION, request_id: str):
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if db_request and db_request.status == RequestStatus.PENDING:
        account = await get_account_by_customer_id(db, db_request.account_id)
        if db_request.type == "DEPOSIT":
            ...
            # account.balance += db_request.amount
        elif db_request.type == "WITHDRAW" and account.balance >= db_request.amount:
            ...
            # account.balance -= db_request.amount
        else:
            return None
        db_request.status = RequestStatus.APPROVED
        db.commit()
        db.refresh(db_request)
        return db_request
    return None


async def get_requests(db: DB_SESSION):
    return db.exec(select(Request)).all()


async def get_requests_by_uuid(session: DB_SESSION, request: FastAPIRequest):
    userinfo = request.state.auth_data
    return session.exec(
        select(Request).where(Request.uuid == int(userinfo["uuid"]))
    ).all()
