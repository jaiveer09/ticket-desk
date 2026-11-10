from fastapi.testclient import TestClient

from app.main import app


def test_list_tickets_is_empty(client: TestClient) -> None:
    response = client.get("/tickets")
    assert response.status_code == 200
    assert response.json() == []


def test_create_ticket_returns_saved_ticket(client: TestClient) -> None:
    response = client.post(
        "/tickets",
        json={
            "title": "Printer jam on floor 2",
            "description": "The shared printer will not pull paper.",
            "status": "open",
            "priority": "high",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Printer jam on floor 2"
    assert body["description"] == "The shared printer will not pull paper."
    assert body["status"] == "open"
    assert body["priority"] == "high"
    assert body["created_at"]


def test_list_tickets_returns_created_tickets(client: TestClient) -> None:
    client.post("/tickets", json={"title": "Reset lobby badge"})
    client.post("/tickets", json={"title": "Replace conference cable", "priority": "low"})

    response = client.get("/tickets")
    assert response.status_code == 200
    titles = [ticket["title"] for ticket in response.json()]
    assert titles == ["Reset lobby badge", "Replace conference cable"]
