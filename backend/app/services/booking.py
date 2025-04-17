from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.booking import BookingRepository
from app.schemas.booking import BookingCreate, BookingStatus
from app.db.models.booking import Booking
from sqlalchemy import select, and_
from fastapi import  HTTPException

class BookingService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = BookingRepository(session)

    async def create_booking(self, data: BookingCreate, user_id: int) -> Booking:
        if await self.is_conflicting(data.room_id, data.start_time, data.end_time):
            raise HTTPException(status_code=400, detail="Time slot is already booked")
        booking = Booking(**data.model_dump(), user_id=user_id)
        return await self.repo.create(booking)

    async def get_all(self) -> list[Booking]:
        return await self.repo.get_all()

    async def get_by_id(self, booking_id: int) -> Booking | None:
        return await self.repo.get_by_id(booking_id)

    async def is_conflicting(self, room_id: int, start, end) -> bool:
        stmt = select(Booking).where(
            Booking.room_id == room_id,
            Booking.status == BookingStatus.approved,
            and_(
                Booking.start_time < end,
                Booking.end_time > start
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
