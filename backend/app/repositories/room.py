from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.room import Room

class RoomRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Room]:
        result = await self.session.execute(select(Room))
        return result.scalars().all()

    async def get_by_id(self, room_id: int) -> Room | None:
        result = await self.session.execute(select(Room).where(Room.id == room_id))
        return result.scalar_one_or_none()

    async def create(self, room: Room) -> Room:
        self.session.add(room)
        await self.session.commit()
        await self.session.refresh(room)
        return room

    async def delete(self, room: Room) -> None:
        await self.session.delete(room)
        await self.session.commit()
