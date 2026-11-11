from typing import Literal

from pydantic import BaseModel, Field, field_validator

Status = Literal["open", "in_progress", "closed"]
Priority = Literal["low", "medium", "high"]


class TicketCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""
    status: Status = "open"
    priority: Priority = "medium"

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("title is required")
        return stripped


class Ticket(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    created_at: str
