from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.booking import Booking

class BookingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, booking_id: int) -> Booking | None:
        result = await self.session.execute(select(Booking).where(Booking.id == booking_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Booking]:
        result = await self.session.execute(select(Booking))
        return result.scalars().all()

    async def create(self, booking: Booking) -> Booking:
        self.session.add(booking)
        await self.session.commit()
        await self.session.refresh(booking)
        return booking
