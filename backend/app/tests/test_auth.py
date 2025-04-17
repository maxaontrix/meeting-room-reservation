import pytest
from app.tests.utils import get_user_payload

@pytest.mark.anyio
async def test_login_user(client):
    payload = get_user_payload("login_user")
    await client.post("/users/", json=payload)
    res = await client.post("/auth/login", data={
        "username": payload["username"],
        "password": payload["password"]
    })
    assert res.status_code == 200
    assert "access_token" in res.json()
