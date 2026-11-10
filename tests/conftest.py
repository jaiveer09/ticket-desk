import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("TICKET_DB_PATH", str(tmp_path / "test.db"))
    with TestClient(app_import()) as test_client:
        yield test_client


def app_import():
    from app.main import app

    return app
