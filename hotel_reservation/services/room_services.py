from datetime import date, timedelta

from sqlalchemy.orm import Session

from hotel_reservation.controllers.schemas.room_schema import (
    RoomAvailabilityDatesSchema,
)
from hotel_reservation.models.room import RoomDAO


class RoomServices:
    def __init__(self, session: Session):
        self.session = session
        self.room_model = RoomDAO(session)

    def check_availability(self) -> RoomAvailabilityDatesSchema:
        start_date = date.today()
        end_date = start_date + timedelta(days=30)
        date_period_set = {start_date + timedelta(days=i) for i in range(30)}

        room = self.room_model.get_room()
        booked_dates = self.room_model.get_room_booked_dates(
            start_date, end_date, room.id
        )
        booked_dates_set = {room_reservation.date for room_reservation in booked_dates}
        available_days = list(date_period_set.difference(booked_dates_set))
        available_days.sort()

        return RoomAvailabilityDatesSchema(
            room_number=room.number, available_dates=available_days
        )
