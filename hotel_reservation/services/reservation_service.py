from sqlalchemy.orm import Session

from hotel_reservation.controllers.schemas.reservation_schemas import (
    ReservationRequest,
    ReservationCreated,
)
from hotel_reservation.models.models import Guest
from hotel_reservation.models.reservation import ReservationDAO


class ReservationService:
    def __init__(self, session: Session):
        self.session = session
        self.reservation_dao = ReservationDAO(session=session)

    def create(self, reservation_request: ReservationRequest) -> ReservationCreated:

        guest = Guest(
            id=reservation_request.guest.id,
            full_name=reservation_request.guest.full_name,
            email=reservation_request.guest.email,
            phone_number=reservation_request.guest.phone_number,
        )

        created_reservation = self.reservation_dao.create(
            reservation_dates=reservation_request.dates,
            observations=reservation_request.observations,
            room_id=reservation_request.room_id,
            guest=guest,
        )

        return ReservationCreated(confirmation_number=created_reservation.id)
