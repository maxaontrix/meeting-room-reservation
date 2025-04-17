from fastapi import FastAPI
from app.api.v1 import room, user, booking, auth

app = FastAPI(title="Meeting Room Reservation")

app.include_router(room.router, prefix="/rooms", tags=["Rooms"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(booking.router, prefix="/bookings", tags=["Bookings"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
