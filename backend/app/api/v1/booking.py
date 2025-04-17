from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.booking import BookingCreate, BookingRead
from app.services.booking import BookingService
from app.db.session import get_session
from app.core.security import get_current_user
from app.db.models.user import User
from app.schemas.user import UserRole
from app.schemas.booking import BookingStatus


router = APIRouter()

@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
async def create_booking(
    data: BookingCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(session)
    return await service.create_booking(data, current_user.id)


@router.get("/", response_model=list[BookingRead])
async def list_bookings(session: AsyncSession = Depends(get_session)):
    service = BookingService(session)
    return await service.get_all()


@router.patch("/{booking_id}/approve", response_model=BookingRead)
async def approve_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.value != UserRole.moderator.value:
        # print(repr(current_user.role))
        # print(repr(UserRole.moderator))
        # print(current_user.role == UserRole.moderator)
        # print(current_user.role is UserRole.moderator)
        # print(current_user.role.value == UserRole.moderator.value)
        raise HTTPException(status_code=403, detail="Only moderators can approve bookings")

    service = BookingService(session)
    booking = await service.get_by_id(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status = BookingStatus.approved
    await session.commit()
    await session.refresh(booking)
    return booking

@router.patch("/{booking_id}/reject", response_model=BookingRead)
async def reject_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.value != UserRole.moderator.value:
        raise HTTPException(status_code=403, detail="Only moderators can reject bookings")

    service = BookingService(session)
    booking = await service.get_by_id(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status = BookingStatus.rejected
    await session.commit()
    await session.refresh(booking)
    return booking
