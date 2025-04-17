import pytest
from app.tests.utils import get_user_payload

@pytest.mark.anyio
async def test_user_cannot_approve(client):
    # создаём обычного пользователя
    user = get_user_payload("notamod")
    await client.post("/users/", json=user)
    login = await client.post("/auth/login", data={
        "username": user["username"],
        "password": user["password"]
    })
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # создаём бронь (любой id)
    res = await client.patch("/bookings/1/approve", headers=headers)

    assert res.status_code == 403
    assert res.json()["detail"] == "Only moderators can approve bookings"
