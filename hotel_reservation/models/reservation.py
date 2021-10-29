from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hotel_reservation.exceptions.reservation_exceptions import (
    DuplicatedReservationError,
)
from hotel_reservation.models.model_base_dao import ModelBaseDAO
from hotel_reservation.models.models import Reservation


class ReservationDAO(ModelBaseDAO):
    def __init__(self, session: Session):
        super().__init__(session)

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

    def get_by_id(self, model_id: int) -> Optional[Reservation]:
        return self.session.query(Reservation).get(model_id)
