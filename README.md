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

- `POST /tickets` creates a ticket. Status is `open`, `in_progress`, or `closed`. Priority is `low`, `medium`, or `high`.
- `GET /tickets` lists tickets. Optional `status` and `priority` parameters narrow the list.
- `POST /tickets/{id}/close` marks a ticket closed.

## Tests

```powershell
python -m pytest
```
