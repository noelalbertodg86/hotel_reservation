from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from hotel_reservation.controllers.reservation.schemas.guest_schema import Guest


class ReservationBase(BaseModel):
    dates: List[date]
    guest: Guest
    room_id: int
    observations: Optional[str]


class ReservationRequest(ReservationBase):
    class Config:
        orm_mode = True


class ReservationCreated(BaseModel):
    confirmation_number: int

    class Config:
        orm_mode = True
