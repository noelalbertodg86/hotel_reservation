from datetime import date as DATE
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hotel_reservation.exceptions.duplicated_reservation import (
    DuplicatedReservationError,
)
from hotel_reservation.models.models import Guest, Reservation, RoomReservation


class ReservationDAO:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        reservation_dates: List[DATE],
        observations: str,
        room_id: int,
        guest: Guest,
    ):
        try:
            room_reservations = [
                RoomReservation(date=date, room_id=room_id)
                for date in reservation_dates
            ]

            reservation = Reservation(
                observations=observations,
                rooms=room_reservations,
                guest=guest,
            )
            self.session.add(reservation)
            self.session.commit()
            return reservation
        except IntegrityError as error:
            self.session.rollback()
            raise DuplicatedReservationError(
                room=room_id, dates=reservation_dates
            ) from error
        except Exception as unexpected_error:
            self.session.rollback()
            raise unexpected_error
