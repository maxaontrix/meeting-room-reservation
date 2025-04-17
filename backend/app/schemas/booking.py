from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class BookingStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class BookingBase(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingRead(BookingBase):
    id: int
    status: BookingStatus
    user_id: int

    class Config:
        from_attributes = True
