from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import connect, init_db
from app.schemas import Ticket, TicketCreate


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Ticket Desk", lifespan=lifespan)


@app.post("/tickets", response_model=Ticket, status_code=201)
def create_ticket(payload: TicketCreate) -> Ticket:
    with connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tickets (title, description, status, priority)
            VALUES (?, ?, ?, ?)
            """,
            (payload.title, payload.description, payload.status, payload.priority),
        )
        row = connection.execute(
            "SELECT * FROM tickets WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return Ticket(**dict(row))


@app.get("/tickets", response_model=list[Ticket])
def list_tickets() -> list[Ticket]:
    with connect() as connection:
        rows = connection.execute(
            "SELECT * FROM tickets ORDER BY id"
        ).fetchall()
    return [Ticket(**dict(row)) for row in rows]
