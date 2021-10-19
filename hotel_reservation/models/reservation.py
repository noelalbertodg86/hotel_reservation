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

    def update(self, reservation_id: int, new_reservation: Reservation) -> Reservation:
        try:
            actual_reservation = self.get_reservation_by_id(reservation_id)
            if not actual_reservation:
                raise NotFoundReservationError(reservation_id)

            actual_reservation.observations = new_reservation.observations
            actual_reservation.guest.full_name = new_reservation.guest.full_name
            actual_reservation.guest.email = new_reservation.guest.email
            actual_reservation.guest.phone_number = new_reservation.guest.phone_number

            for room_reservation in actual_reservation.room_reservations:
                self.session.delete(room_reservation)

            actual_reservation.room_reservations = new_reservation.room_reservations
            self.session.merge(actual_reservation)
            self.session.commit()
            return actual_reservation
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
