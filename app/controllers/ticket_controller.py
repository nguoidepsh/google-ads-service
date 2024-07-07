
from fastapi import HTTPException
from sqlmodel import select # type: ignore
from db.db_connector import DB_SESSION
from models import Ticket, TicketCreate, TicketRead


async def create(ticket: TicketCreate, session: DB_SESSION):
    if not ticket.tasks:
        raise HTTPException(status_code=400, detail="A ticket must have at least one task")
    db_ticket = Ticket.from_orm(ticket)
    session.add(db_ticket)
    session.commit()
    session.refresh(db_ticket)
    return db_ticket

    
def get(session: DB_SESSION):
    tickets = session.exec(select(Ticket)).all()
    return tickets