from datetime import date
from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from hotel_reservation.models.model_base_dao import ModelBaseDAO
from hotel_reservation.models.models import Room, RoomReservation


class RoomDAO(ModelBaseDAO):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_room_booked_dates(
        self, start_date: date, end_date: date, room_id: int
    ) -> List[RoomReservation]:
        reservation_dates = (
            self.session.query(RoomReservation)
            .filter(
                and_(
                    RoomReservation.date >= start_date,
                    RoomReservation.date <= end_date,
                    RoomReservation.room_id == room_id,
                )
            )
            .all()
        )
        return reservation_dates

    def get_by_id(self, room_id: int = 0) -> Room:
        if room_id:
            return self.session.query(Room).get(room_id)
        return self.session.query(Room).first()
