from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.room import RoomRepository
from app.schemas.room import RoomCreate, RoomUpdate
from app.db.models.room import Room

class RoomService:
    def __init__(self, session: AsyncSession):
        self.repo = RoomRepository(session)

    async def get_all(self) -> list[Room]:
        return await self.repo.get_all()

    async def get_by_id(self, room_id: int) -> Room | None:
        return await self.repo.get_by_id(room_id)

    async def create(self, room_data: RoomCreate) -> Room:
        room = Room(**room_data.model_dump())
        return await self.repo.create(room)

    async def update(self, room_id: int, data: RoomUpdate) -> Room | None:
        room = await self.repo.get_by_id(room_id)
        if not room:
            return None
        for field, value in data.model_dump().items():
            setattr(room, field, value)
        return await self.repo.create(room)  # т.к. create = upsert

    async def delete(self, room_id: int) -> bool:
        room = await self.repo.get_by_id(room_id)
        if not room:
            return False
        await self.repo.delete(room)
        return True
