from pydantic import BaseModel

class RoomBase(BaseModel):
    name: str
    location: str
    capacity: int

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    pass

class RoomRead(RoomBase):
    id: int

    class Config:
        from_attributes = True
