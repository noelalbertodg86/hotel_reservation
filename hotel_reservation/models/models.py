import enum

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
    Enum,
    Boolean,
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
    room_id = Column(
        ForeignKey("room.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    )
    reservation_id = Column(
        ForeignKey("reservation.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )

    room = relationship("Room", back_populates="reservations")
    reservation = relationship("Reservation", back_populates="room_reservations")

    __table_args__ = (
        UniqueConstraint("date", "room_id", name="reservation_unique_day"),
    )


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, autoincrement=True, primary_key=True)
    number = Column(Integer)
    type = Column(String(50), server_default="Simple")
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
    room_reservations = relationship(
        "RoomReservation", back_populates="reservation", cascade="all, delete"
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def get_dates_to_str(self):
        return list(map(str, self.get_dates()))

    def get_dates(self):
        return [room_reservation.date for room_reservation in self.room_reservations]


class Guest(Base):
    __tablename__ = "guest"
    id = Column(String(25), primary_key=True)
    full_name = Column(String(200))
    email = Column(String(50))
    phone_number = Column(BigInteger)
    reservation = relationship("Reservation", back_populates="guest")


class ReservationRulesCodes(enum.Enum):
    RESERVE_MAX_ALLOWED_DAYS = "RESERVE_MAX_ALLOWED_DAYS"
    RESERVE_MAX_ALLOWED_BOOKING_IN_ADVANCE_DAYS = (
        "RESERVE_MAX_ALLOWED_BOOKING_IN_ADVANCE_DAYS"
    )
    RESERVE_MIN_ALLOWED_DAYS_BETWEEN_BOOK_AND_RESERVATION_BEGIN = (
        "RESERVE_MIN_ALLOWED_DAYS_BETWEEN_BOOK_AND_RESERVATION_BEGIN"
    )


class ReservationRules(Base):
    __tablename__ = "reservation_rules"
    id = Column(Integer, autoincrement=True, primary_key=True)
    code = Column(Enum(ReservationRulesCodes), nullable=False, unique=True)
    value = Column(Integer)
    active = Column(Boolean, server_default="1")
