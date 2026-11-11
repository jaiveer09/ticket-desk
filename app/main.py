from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.database import connect, init_db
from app.schemas import Priority, Status, Ticket, TicketCreate


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
def list_tickets(
    status: Status | None = None,
    priority: Priority | None = None,
) -> list[Ticket]:
    query = "SELECT * FROM tickets WHERE 1 = 1"
    parameters: list[str] = []
    if status is not None:
        query += " AND status = ?"
        parameters.append(status)
    if priority is not None:
        query += " AND priority = ?"
        parameters.append(priority)
    query += " ORDER BY id"

    with connect() as connection:
        rows = connection.execute(query, parameters).fetchall()
    return [Ticket(**dict(row)) for row in rows]


@app.post("/tickets/{ticket_id}/close", response_model=Ticket)
def close_ticket(ticket_id: int) -> Ticket:
    with connect() as connection:
        cursor = connection.execute(
            "UPDATE tickets SET status = 'closed' WHERE id = ?",
            (ticket_id,),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Ticket not found")
        row = connection.execute(
            "SELECT * FROM tickets WHERE id = ?",
            (ticket_id,),
        ).fetchone()
    return Ticket(**dict(row))
