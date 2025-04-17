import pytest
from app.tests.utils import get_user_payload
from datetime import datetime, timedelta

@pytest.mark.anyio
async def test_create_booking(client):
    # создаём пользователя
    payload = get_user_payload("booker")
    await client.post("/users/", json=payload)
    login = await client.post("/auth/login", data={
        "username": payload["username"],
        "password": payload["password"]
    })
    token = login.json()["access_token"]

    # создаём комнату
    room_data = {"name": "Bookable Room", "location": "2nd", "capacity": 5}
    room = await client.post("/rooms/", json=room_data)
    room_id = room.json()["id"]

    # создаём бронь
    headers = {"Authorization": f"Bearer {token}"}
    now = datetime.utcnow()
    start = (now + timedelta(hours=1)).isoformat()
    end = (now + timedelta(hours=2)).isoformat()

    booking_payload = {
        "room_id": room_id,
        "start_time": start,
        "end_time": end
    }
    res = await client.post("/bookings/", json=booking_payload, headers=headers)
    assert res.status_code == 201
    assert res.json()["status"] == "pending"
