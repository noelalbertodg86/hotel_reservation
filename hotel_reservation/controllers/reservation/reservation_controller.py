from fastapi import APIRouter, Response, status

from database import session_factory
from hotel_reservation.controllers.reservation.schemas.reservation_schemas import (
    ReservationRequest,
    ReservationCreated,
)
from hotel_reservation.services.reservation_service import ReservationService

router = APIRouter()

db_session = session_factory()
reservation_service = ReservationService(session=db_session)


@router.get("/healthcheck", tags=["healthcheck"])
def health_check():
    return {"status": "UP"}


@router.post("/reservation/", response_model=ReservationCreated)
def create_user(response: Response, reservation: ReservationRequest):
    response.status_code = status.HTTP_201_CREATED
    return reservation_service.create(reservation)
