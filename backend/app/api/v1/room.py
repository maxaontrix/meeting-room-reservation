from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.room import RoomService
from app.schemas.room import RoomCreate, RoomRead, RoomUpdate
from app.db.session import get_session

router = APIRouter()

@router.get("/", response_model=list[RoomRead])
async def list_rooms(session: AsyncSession = Depends(get_session)):
    service = RoomService(session)
    return await service.get_all()

@router.get("/{room_id}", response_model=RoomRead)
async def get_room(room_id: int, session: AsyncSession = Depends(get_session)):
    service = RoomService(session)
    room = await service.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.post("/", response_model=RoomRead, status_code=201)
async def create_room(data: RoomCreate, session: AsyncSession = Depends(get_session)):
    service = RoomService(session)
    return await service.create(data)

@router.put("/{room_id}", response_model=RoomRead)
async def update_room(room_id: int, data: RoomUpdate, session: AsyncSession = Depends(get_session)):
    service = RoomService(session)
    updated = await service.update(room_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Room not found")
    return updated

@router.delete("/{room_id}", status_code=204)
async def delete_room(room_id: int, session: AsyncSession = Depends(get_session)):
    service = RoomService(session)
    success = await service.delete(room_id)
    if not success:
        raise HTTPException(status_code=404, detail="Room not found")
