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


def test_filter_tickets_by_status_and_priority(client: TestClient) -> None:
    client.post("/tickets", json={"title": "Open high", "status": "open", "priority": "high"})
    client.post("/tickets", json={"title": "Open low", "status": "open", "priority": "low"})
    client.post(
        "/tickets",
        json={"title": "Working high", "status": "in_progress", "priority": "high"},
    )

    by_status = client.get("/tickets", params={"status": "open"})
    assert [ticket["title"] for ticket in by_status.json()] == ["Open high", "Open low"]

    by_priority = client.get("/tickets", params={"priority": "high"})
    assert [ticket["title"] for ticket in by_priority.json()] == ["Open high", "Working high"]

    both = client.get("/tickets", params={"status": "open", "priority": "high"})
    assert [ticket["title"] for ticket in both.json()] == ["Open high"]


def test_close_ticket(client: TestClient) -> None:
    created = client.post("/tickets", json={"title": "Badge printer"}).json()

    response = client.post(f"/tickets/{created['id']}/close")
    assert response.status_code == 200
    assert response.json()["status"] == "closed"

    listed = client.get("/tickets", params={"status": "closed"})
    assert listed.json()[0]["title"] == "Badge printer"


def test_close_missing_ticket(client: TestClient) -> None:
    response = client.post("/tickets/999/close")
    assert response.status_code == 404


def test_reject_invalid_ticket_input(client: TestClient) -> None:
    missing_title = client.post("/tickets", json={"description": "No title"})
    blank_title = client.post("/tickets", json={"title": "   "})
    bad_status = client.post("/tickets", json={"title": "Desk move", "status": "done"})
    bad_priority = client.post("/tickets", json={"title": "Desk move", "priority": "urgent"})
    bad_filter = client.get("/tickets", params={"status": "done"})

    assert missing_title.status_code == 422
    assert blank_title.status_code == 422
    assert bad_status.status_code == 422
    assert bad_priority.status_code == 422
    assert bad_filter.status_code == 422
