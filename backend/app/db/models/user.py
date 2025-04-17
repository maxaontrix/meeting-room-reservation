from sqlalchemy import Column, String, Integer, Enum
from app.db.base_class import Base
import enum

class UserRole(enum.Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
