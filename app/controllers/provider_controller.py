from db.db_connector import DB_SESSION
from fastapi import Depends, Request
from models.provider_model import Provider, ProviderCreate, ProviderUpdate
from sqlmodel import select
from starlette.exceptions import HTTPException


async def get_all(session: DB_SESSION):
    return session.exec(select(Provider)).all()


# GET Provider by ID
async def get_provider_by_id(session: DB_SESSION, id: str):
    provider = session.exec(select(Provider).where(Provider.id == id)).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

# CREATE a new Provider


async def create_provider(session: DB_SESSION, provider_data: ProviderCreate):
    provider = Provider(**provider_data.model_dump())
    session.add(provider)
    session.commit()
    session.refresh(provider)
    return provider

# UPDATE an existing Provider


async def update_provider(session: DB_SESSION, updates: ProviderUpdate):
    provider = session.exec(select(Provider).where(
        Provider.id == updates.id)).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    update_data = updates.model_dump()

    for key, value in update_data.items():
        setattr(provider, key, value)

    session.add(provider)
    session.commit()
    session.refresh(provider)
    return provider

# DELETE a Provider


async def delete_provider(session: DB_SESSION, id: str):
    provider = session.exec(select(Provider).where(Provider.id == id)).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    session.delete(provider)
    session.commit()
    return {"message": "Provider deleted successfully"}
