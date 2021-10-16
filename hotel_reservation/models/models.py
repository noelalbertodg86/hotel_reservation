from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Date,
    func,
    DateTime,
    BigInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Hotel(Base):
    __tablename__ = "hotel"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(250))
    address = Column(String(250))
    rooms = relationship("Room", back_populates="hotel")


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, autoincrement=True, primary_key=True)
    number = Column(Integer)
    hotel_id = Column(Integer, ForeignKey("hotel.id"), nullable=False)
    hotel = relationship("Hotel", back_populates="rooms")
    reservations = relationship("Reservation", back_populates="room")


class Reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, autoincrement=True, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    room_id = Column(Integer, ForeignKey("room.id"), nullable=False)
    room = relationship("Room", back_populates="reservation")
    guest_id = Column(String(25), ForeignKey("guest.id"), nullable=False)
    guest = relationship("Guest", back_populates="reservation")
    dates = relationship("ReservationDate", back_populates="reservation")


class ReservationDate(Base):
    __tablename__ = "reservation_date"
    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(Date, nullable=False)
    reservation_id = Column(Integer, ForeignKey("reservation.id"), nullable=False)
    reservation = relationship("Reservation", back_populates="reservation_date")
    __table_args__ = (
        UniqueConstraint("date", "reservation_id", name="reservation_unique_day"),
    )


class Guest(Base):
    __tablename__ = "guest"
    id = Column(String(25), primary_key=True)
    full_name = Column(String(200))
    email = Column(String(50))
    phone_number = Column(BigInteger)
    reservations = relationship("Reservation", back_populates="guest")
