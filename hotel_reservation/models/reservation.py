from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hotel_reservation.exceptions.reservation_exceptions import (
    DuplicatedReservationError,
)
from hotel_reservation.exceptions.reservation_exceptions import NotFoundReservationError
from hotel_reservation.models.models import Reservation, RoomReservation


class ReservationDAO:
    def __init__(self, session: Session):
        self.session = session

    def create(self, reservation: Reservation) -> Reservation:
        try:
            self.session.add(reservation)
            self.session.commit()
            return reservation
        except IntegrityError as error:
            self.session.rollback()
            raise DuplicatedReservationError(reservation=reservation) from error
        except Exception as unexpected_error:
            self.session.rollback()
            raise unexpected_error

    def update(self, reservation: Reservation) -> Reservation:
        try:
            self.session.merge(reservation)
            self.session.commit()
            return reservation
        except Exception as error:
            self.session.rollback()
            raise error

    def get_reservation_by_id(self, reservation_id: int) -> Optional[Reservation]:
        return self.session.query(Reservation).get(reservation_id)

    def delete(self, reservation: Reservation) -> Reservation:
        try:
            self.session.delete(reservation)
            self.session.commit()
            return reservation
        except Exception as deleted_error:
            self.session.rollback()
            raise deleted_error
