
from fastapi import HTTPException
from sqlmodel import select # type: ignore
from db.db_connector import DB_SESSION
from models.stat_model import SearchTermStat, SearchTermCreate


async def create(data: SearchTermCreate, session: DB_SESSION):
    try:
        # Verify that token details are provided
        values = data.dict()
        stat = SearchTermStat(**values)
        session.add(stat)
        session.commit()
        session.refresh(stat)
        return stat

    except Exception as e:
        print("Error while creating Stat:", e)
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the stat."
        )
    
# def get(session: DB_SESSION):
#     tokens = session.exec(select(Token)).all()
#     if tokens:
#         return tokens
#     raise HTTPException(status_code=404, detail="Stat not found")