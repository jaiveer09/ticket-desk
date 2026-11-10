from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""
    status: str = "open"
    priority: str = "medium"


class Ticket(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    created_at: str
