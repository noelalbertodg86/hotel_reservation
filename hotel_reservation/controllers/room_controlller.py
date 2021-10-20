from fastapi import APIRouter, Response, status

from database import session_factory
from hotel_reservation.controllers.schemas.room_schema import (
    RoomAvailabilityDatesSchema,
)
from hotel_reservation.services.room_services import RoomServices

router = APIRouter()
db_session = session_factory()


@router.get("/healthcheck", tags=["healthcheck"])
def health_check():
    return {"status": "UP"}


@router.get(
    "/v1/room/availability/{room_id}", response_model=RoomAvailabilityDatesSchema
)
def get_availability(response: Response, room_id: int):
    room_services = RoomServices(db_session)
    response.status_code = status.HTTP_200_OK
    return room_services.check_availability(room_id)
