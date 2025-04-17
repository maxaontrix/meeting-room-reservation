import pytest

@pytest.mark.anyio
async def test_create_room(client):
    room_data = {
        "name": "Test Room",
        "location": "1st Floor",
        "capacity": 10
    }
    res = await client.post("/rooms/", json=room_data)
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Test Room"
    assert data["location"] == "1st Floor"

@pytest.mark.anyio
async def test_get_all_rooms(client):
    res = await client.get("/rooms/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
