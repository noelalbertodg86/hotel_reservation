from fastapi import APIRouter, Response, status, Depends
from sqlalchemy.orm import Session

from hotel_reservation.controllers.schemas.reservation_schemas import (
    ReservationRequestSchema,
    ReservationCreatedSchema,
    ReservationUpdatedSchema,
    ReservationDeletedSchema,
    ReservationSelectedSchema,
)
from hotel_reservation.database import get_db
from hotel_reservation.services.reservation_service import ReservationService

router = APIRouter()


@router.get(
    "/v1/reservation/{confirmation_number}", response_model=ReservationSelectedSchema
)
def get_reservation(confirmation_number: int, db: Session = Depends(get_db)):
    return ReservationService(session=db).get_reservation(confirmation_number)


@router.post("/v1/reservation/", response_model=ReservationCreatedSchema)
def create_reservation(
    response: Response,
    reservation: ReservationRequestSchema,
    db: Session = Depends(get_db),
):
    response.status_code = status.HTTP_201_CREATED
    return ReservationService(session=db).create(reservation)


@router.put(
    "/v1/reservation/{confirmation_number}", response_model=ReservationUpdatedSchema
)
def update_reservation(
    response: Response,
    confirmation_number: int,
    reservation: ReservationRequestSchema,
    db: Session = Depends(get_db),
):
    response.status_code = status.HTTP_200_OK
    return ReservationService(session=db).update(reservation, confirmation_number)


@router.delete(
    "/v1/reservation/{confirmation_number}", response_model=ReservationDeletedSchema
)
def delete_reservation(
    response: Response, confirmation_number: int, db: Session = Depends(get_db)
):
    response.status_code = status.HTTP_200_OK
    return ReservationService(session=db).delete(confirmation_number)
