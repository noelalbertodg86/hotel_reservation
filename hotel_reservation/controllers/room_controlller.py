from fastapi import APIRouter, Response, status, Depends
from sqlalchemy.orm import Session

from hotel_reservation.controllers.schemas.room_schema import (
    RoomAvailabilityDatesSchema,
)
from hotel_reservation.database import get_db
from hotel_reservation.services.room_services import RoomServices

router = APIRouter()


@router.get(
    "/v1/room/availability/{room_id}", response_model=RoomAvailabilityDatesSchema
)
def get_availability(response: Response, room_id: int, db: Session = Depends(get_db)):
    response.status_code = status.HTTP_200_OK
    return RoomServices(db).check_availability(room_id)
