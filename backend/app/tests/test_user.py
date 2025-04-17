import pytest
from app.tests.utils import get_user_payload

@pytest.mark.anyio
async def test_register_user(client):
    payload = get_user_payload("user_test")
    res = await client.post("/users/", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["username"] == payload["username"]

@pytest.mark.anyio
async def test_register_duplicate_user(client):
    payload = get_user_payload("duplicate_user")
    await client.post("/users/", json=payload)
    res = await client.post("/users/", json=payload)
    assert res.status_code == 400
    assert res.json()["detail"] == "Username already exists"
