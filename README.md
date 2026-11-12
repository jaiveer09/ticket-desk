# Ticket Desk

A small API that stores support tickets. Each ticket has a title, an optional description, a status, and a priority. The tickets are saved in a SQLite database file.

## Endpoints

The API listens on port 8000. Interactive docs are at `/docs`.

- `POST /tickets` creates a ticket. Status is `open`, `in_progress`, or `closed`. Priority is `low`, `medium`, or `high`.
- `GET /tickets` lists tickets. Optional `status` and `priority` query parameters narrow the list.
- `POST /tickets/{id}/close` marks a ticket closed. An unknown id returns 404.

A blank title, or a status or priority outside those values, returns 422.

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Tests

```powershell
python -m pytest
```

GitHub Actions runs the same command on every push to `main`.

## Docker

Build and run the API:

```powershell
docker build -t ticket-desk .
docker run --rm -p 8000:8000 ticket-desk
```

Open `http://127.0.0.1:8000/docs`. The database file lives inside the container and is removed when the container stops.
