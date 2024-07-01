
from fastapi import HTTPException
from sqlmodel import select # type: ignore
from db.db_connector import DB_SESSION
from models.offer_model import Offer, OfferCreate, OfferRead


async def create(data: OfferCreate, session: DB_SESSION):
    try:
        # Verify that token details are provided
        values = data.model_dump()
        stat = Offer(**values)
        session.add(stat)
        session.commit()
        session.refresh(stat)
        return stat

    except Exception as e:
        print("Error while creating Offer:", e)
        raise HTTPException(
            status_code=500, detail="An error occurred while creating offer."
        )
    
def get(session: DB_SESSION):
    offers = session.exec(select(Offer)).all()
    if offers:
        return offers
    raise HTTPException(status_code=404, detail="Offer not found")