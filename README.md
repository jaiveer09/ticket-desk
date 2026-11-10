# Ticket Desk

A small API for creating and listing support tickets.

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The API listens on `http://127.0.0.1:8000`.

- `POST /tickets` creates a ticket.
- `GET /tickets` lists tickets.

## Tests

```powershell
python -m pytest
```
