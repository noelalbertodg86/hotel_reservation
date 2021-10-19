from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from hotel_reservation.controllers.schemas.guest_schema import GuestSchema
from hotel_reservation.models.models import Reservation


class ReservationBase(BaseModel):
    dates: List[date]
    guest: GuestSchema
    room_id: int
    observations: Optional[str]


class ReservationRequestSchema(ReservationBase):
    class Config:
        orm_mode = True


class ReservationCreatedSchema(ReservationBase):
    confirmation_number: int
    message: str = "Reservation created successfully"

    class Config:
        orm_mode = True

    @staticmethod
    def build_from_reservation_model(reservation: Reservation):
        return ReservationCreatedSchema(
            dates=reservation.get_dates(),
            guest=GuestSchema.build_from_guest_data_model(reservation.guest),
            room_id=reservation.room_reservations[0].room.id,
            observations=reservation.observations,
            confirmation_number=reservation.id,
        )


class ReservationUpdatedSchema(ReservationBase):
    confirmation_number: int
    message: str = "Reservation updated successfully"

    class Config:
        orm_mode = True

    @staticmethod
    def build_from_reservation_model(reservation: Reservation):
        return ReservationUpdatedSchema(
            dates=reservation.get_dates(),
            guest=GuestSchema.build_from_guest_data_model(reservation.guest),
            room_id=reservation.room_reservations[0].room.id,
            observations=reservation.observations,
            confirmation_number=reservation.id,
        )


class ReservationDeletedSchema(BaseModel):
    confirmation_number: int
    message: str = "Reservation deleted successfully"


class ReservationSelectedSchema(ReservationCreatedSchema):
    pass
