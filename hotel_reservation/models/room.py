from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, autoincrement=True, primary_key=True)
    number = Column(Integer)
    hotel_id = Column(Integer, ForeignKey("hotel.id"), nullable=False)
    hotel = relationship("Hotel", back_populates="rooms")
