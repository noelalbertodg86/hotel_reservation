from fastapi import APIRouter, Response, status

from hotel_reservation.database import session_factory
from hotel_reservation.controllers.schemas.reservation_schemas import (
    ReservationRequestSchema,
    ReservationCreatedSchema,
    ReservationUpdatedSchema,
    ReservationDeletedSchema,
    ReservationSelectedSchema,
)
from hotel_reservation.services.reservation_service import ReservationService

router = APIRouter()

db_session = session_factory()
reservation_service = ReservationService(session=db_session)


@router.get(
    "/v1/reservation/{confirmation_number}", response_model=ReservationSelectedSchema
)
def get_reservation(confirmation_number: int):
    return reservation_service.get_reservation(confirmation_number)


@router.post("/v1/reservation/", response_model=ReservationCreatedSchema)
def create_reservation(response: Response, reservation: ReservationRequestSchema):
    response.status_code = status.HTTP_201_CREATED
    return reservation_service.create(reservation)


@router.put(
    "/v1/reservation/{confirmation_number}", response_model=ReservationUpdatedSchema
)
def update_reservation(
    response: Response, confirmation_number: int, reservation: ReservationRequestSchema
):
    response.status_code = status.HTTP_200_OK
    return reservation_service.update(reservation, confirmation_number)


@router.delete(
    "/v1/reservation/{confirmation_number}", response_model=ReservationDeletedSchema
)
def delete_reservation(response: Response, confirmation_number: int):
    response.status_code = status.HTTP_200_OK
    return reservation_service.delete(confirmation_number)
