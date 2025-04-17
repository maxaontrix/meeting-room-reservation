from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
