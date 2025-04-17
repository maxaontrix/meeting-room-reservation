from sqlalchemy import Column, String, Integer
from app.db.base_class import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    location = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
