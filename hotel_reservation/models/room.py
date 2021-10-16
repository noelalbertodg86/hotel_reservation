from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship

from hotel_reservation.models import Base


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, autoincrement=True, primary_key=True)
    number = Column(Integer)
    hotel_id = Column(Integer, ForeignKey("hotel.id"))

    hotel = relationship("Hotel", back_populates="rooms")

    def __init__(self, session: Session, number: int):
        self.session = session
        self.number = number

    def save(self):
        self.session.add(self)
        self.session.commit()
