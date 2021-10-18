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
    Numeric,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Hotel(Base):
    __tablename__ = "hotel"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(250))
    address = Column(String(250))
    rooms = relationship("Room", back_populates="hotel")


class RoomReservation(Base):
    __tablename__ = "room_reservation"
    date = Column(Date, primary_key=True)
    room_id = Column(ForeignKey("room.id", ondelete="CASCADE"), primary_key=True)
    reservation_id = Column(
        ForeignKey("reservation.id", ondelete="CASCADE"), primary_key=True
    )

    room = relationship("Room", back_populates="reservations")
    reservation = relationship("Reservation", back_populates="rooms")

    __table_args__ = (
        UniqueConstraint("date", "room_id", name="reservation_unique_day"),
    )


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, autoincrement=True, primary_key=True)
    number = Column(Integer)
    type = Column(String(50), server_default="Simple")
    price_per_day = Column(Numeric(10, 2), server_default="50.50")
    hotel_id = Column(
        Integer, ForeignKey("hotel.id", ondelete="CASCADE"), nullable=False
    )
    hotel = relationship("Hotel", back_populates="rooms")
    reservations = relationship("RoomReservation", back_populates="room")


class Reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, autoincrement=True, primary_key=True)
    observations = Column(String(250), server_default="")
    guest_id = Column(String(25), ForeignKey("guest.id"))
    guest = relationship("Guest", back_populates="reservation")
    rooms = relationship("RoomReservation", back_populates="reservation")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Guest(Base):
    __tablename__ = "guest"
    id = Column(String(25), primary_key=True)
    full_name = Column(String(200))
    email = Column(String(50))
    phone_number = Column(BigInteger)
    reservation = relationship("Reservation", back_populates="guest")
