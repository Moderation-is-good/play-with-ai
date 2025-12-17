import pytest
from fastapi.testclient import TestClient

from src.app import app, read_access, service, write_access

client = TestClient(app)


@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[read_access] = lambda: {
        "realm_access": {"roles": ["books:read", "books:write"]}
    }
    app.dependency_overrides[write_access] = lambda: {
        "realm_access": {"roles": ["books:read", "books:write"]}
    }
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def reset_store():
    service.reset()
    yield
    service.reset()


def test_create_and_get_book():
    payload = {"title": "1984", "author": "Orwell", "price": 9.99, "in_stock": True}
    resp = client.post("/api/v1/books", json=payload)
    assert resp.status_code == 201
    created = resp.json()
    assert created["title"] == "1984"
    assert created["id"] == 1

    resp = client.get(f"/api/v1/books/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["author"] == "Orwell"


def test_update_and_delete_book():
    payload = {"title": "Dune", "author": "Herbert", "price": 12.5, "in_stock": True}
    created = client.post("/api/v1/books", json=payload).json()
    updated = client.put(
        f"/api/v1/books/{created['id']}",
        json={"price": 15.0, "in_stock": False},
    )
    assert updated.status_code == 200
    assert updated.json()["price"] == 15.0
    assert updated.json()["version"] == 2

    deleted = client.delete(f"/api/v1/books/{created['id']}")
    assert deleted.status_code == 204

    missing = client.get(f"/api/v1/books/{created['id']}")
    assert missing.status_code == 404


def test_versioned_listing_sorted():
    client.post("/api/v1/books", json={"title": "B", "author": "X", "price": 1.0, "in_stock": True})
    client.post("/api/v1/books", json={"title": "a", "author": "Y", "price": 1.0, "in_stock": True})

    resp_v2 = client.get("/api/v2/books")
    titles = [item["title"] for item in resp_v2.json()]
    assert titles == sorted(titles, key=lambda t: t.lower())
