from datetime import date, timedelta

from sqlalchemy.orm import Session

from hotel_reservation.controllers.schemas.reservation_schemas import (
    ReservationRequestSchema,
    ReservationCreatedSchema,
    ReservationUpdatedSchema,
    ReservationDeletedSchema,
    ReservationSelectedSchema,
)
from hotel_reservation.exceptions.reservation_exceptions import NotFoundReservationError
from hotel_reservation.models.guest import GuestDAO
from hotel_reservation.models.models import Guest, RoomReservation, Reservation
from hotel_reservation.models.reservation import ReservationDAO


class ReservationService:
    def __init__(self, session: Session):
        self.session = session
        self.reservation_dao = ReservationDAO(session=session)
        self.guest_dao = GuestDAO(session=session)

    def get_reservation(self, confirmation_number: int) -> ReservationSelectedSchema:
        reservation = self.reservation_dao.get_reservation_by_id(
            reservation_id=confirmation_number
        )
        if not reservation:
            raise NotFoundReservationError(confirmation_number)
        return ReservationSelectedSchema.build_from_reservation_model(reservation)

    def create(
        self, reservation_request: ReservationRequestSchema
    ) -> ReservationCreatedSchema:
        guest = self.guest_dao.get_guest_by_id(reservation_request.guest.id)
        if not guest:
            guest = Guest(**reservation_request.guest.dict())

        room_reservations = [
            RoomReservation(date=date, room_id=reservation_request.room_id)
            for date in reservation_request.dates
        ]

        reservation = Reservation(
            observations=reservation_request.observations,
            room_reservations=room_reservations,
            guest=guest,
            guest_id=reservation_request.guest.id,
        )

        created_reservation = self.reservation_dao.create(reservation)

        return ReservationCreatedSchema.build_from_reservation_model(
            created_reservation
        )

    def update(
        self,
        update_reservation_request: ReservationRequestSchema,
        confirmation_number: int,
    ) -> ReservationUpdatedSchema:

        guest = Guest(**update_reservation_request.guest.dict())

        room_reservations = [
            RoomReservation(date=date, room_id=update_reservation_request.room_id)
            for date in update_reservation_request.dates
        ]

        new_reservation = Reservation(
            observations=update_reservation_request.observations,
            room_reservations=room_reservations,
            guest=guest,
            guest_id=guest.id,
        )
        updated_reservation = self.reservation_dao.update(
            confirmation_number, new_reservation
        )

        return ReservationUpdatedSchema.build_from_reservation_model(
            updated_reservation
        )

    def delete(self, confirmation_number: int) -> ReservationDeletedSchema:
        reservation = self.reservation_dao.get_reservation_by_id(confirmation_number)
        if not reservation:
            raise NotFoundReservationError(confirmation_number)

        self.reservation_dao.delete(reservation)
        return ReservationDeletedSchema(confirmation_number=confirmation_number)
