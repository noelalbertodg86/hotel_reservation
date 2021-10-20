from datetime import datetime

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
from hotel_reservation.services.reservation_rules_service import ReservationRulesService


class ReservationService:
    def __init__(self, session: Session):
        self.session = session
        self.reservation_dao = ReservationDAO(session=session)
        self.guest_dao = GuestDAO(session=session)
        self.reservation_rules_validators = ReservationRulesService(
            session
        ).get_rules_validators()

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
        guest = self.guest_dao.get_guest_by_id(reservation_request.guest.identification)
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
            guest_id=reservation_request.guest.identification,
        )

        self.validate_reservation(reservation)

        created_reservation = self.reservation_dao.create(reservation)

        return ReservationCreatedSchema.build_from_reservation_model(
            created_reservation
        )

    def update(
        self,
        update_reservation_request: ReservationRequestSchema,
        confirmation_number: int,
    ) -> ReservationUpdatedSchema:

        reservation_to_update = self.reservation_dao.get_reservation_by_id(
            reservation_id=confirmation_number
        )
        if not reservation_to_update:
            raise NotFoundReservationError(confirmation_number)

        reservation_to_update.observations = update_reservation_request.observations
        reservation_to_update.updated_at = datetime.now()
        reservation_to_update.guest.email = update_reservation_request.guest.email
        reservation_to_update.guest.phone_number = (
            update_reservation_request.guest.phone_number
        )
        reservation_to_update.guest.identification = (
            update_reservation_request.guest.identification
        )
        reservation_to_update.guest.full_name = (
            update_reservation_request.guest.full_name
        )
        for room_reservation in reservation_to_update.room_reservations:
            self.session.delete(room_reservation)

        reservation_to_update.room_reservations = [
            RoomReservation(
                date=reservation_date, room_id=update_reservation_request.room_id
            )
            for reservation_date in update_reservation_request.dates
        ]
        self.validate_reservation(reservation_to_update)
        updated_reservation = self.reservation_dao.update(reservation_to_update)

        return ReservationUpdatedSchema.build_from_reservation_model(
            updated_reservation
        )

    def delete(self, confirmation_number: int) -> ReservationDeletedSchema:
        reservation = self.reservation_dao.get_reservation_by_id(confirmation_number)
        if not reservation:
            raise NotFoundReservationError(confirmation_number)

        self.reservation_dao.delete(reservation)
        return ReservationDeletedSchema(confirmation_number=confirmation_number)

    def validate_reservation(self, reservation: Reservation):
        validation_result = [
            validator.validate(reservation)
            for validator in self.reservation_rules_validators
        ]
        return all(validation_result)
