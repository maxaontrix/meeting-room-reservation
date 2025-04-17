import pytest
from datetime import datetime, timedelta
from app.tests.utils import get_user_payload

@pytest.mark.anyio
async def test_booking_conflict(client):
    # 1. Создание пользователя и логин
    user_data = get_user_payload("conflict_user")
    await client.post("/users/", json=user_data)
    # assert res.status_code == 201

    login_res = await client.post("/auth/login", data={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Создание комнаты
    room_res = await client.post("/rooms/", json={
        "name": "Conflict Room",
        "location": "Somewhere",
        "capacity": 5
    })
    room_id = room_res.json()["id"]

    # 3. Первая бронь: 10:00 - 11:00
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    start_1 = (now + timedelta(hours=1)).isoformat()
    end_1 = (now + timedelta(hours=2)).isoformat()

    booking_1 = await client.post("/bookings/", json={
        "room_id": room_id,
        "start_time": start_1,
        "end_time": end_1
    }, headers=headers)
    assert booking_1.status_code == 201

    # 4. Аппрувим первую бронь через модератора
    mod_data = get_user_payload("conflict_mod", role="moderator")

    await client.post("/users/", json=mod_data)
    # assert res.status_code == 201
    mod_login = await client.post("/auth/login", data={
        "username": mod_data["username"],
        "password": mod_data["password"]
    })
    mod_token = mod_login.json()["access_token"]
    mod_headers = {"Authorization": f"Bearer {mod_token}"}

    booking_id = booking_1.json()["id"]
    approve_res = await client.patch(f"/bookings/{booking_id}/approve", headers=mod_headers)
    assert approve_res.status_code == 200
    assert approve_res.json()["status"] == "approved"

    # 5. Вторая бронь (пересекается): 10:30 - 11:30
    start_2 = (now + timedelta(hours=1, minutes=30)).isoformat()
    end_2 = (now + timedelta(hours=2, minutes=30)).isoformat()

    booking_2 = await client.post("/bookings/", json={
        "room_id": room_id,
        "start_time": start_2,
        "end_time": end_2
    }, headers=headers)

    # 6. Проверка конфликта
    assert booking_2.status_code == 400
    assert booking_2.json()["detail"] == "Time slot is already booked"
