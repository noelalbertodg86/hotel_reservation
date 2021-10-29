from datetime import date, timedelta

from sqlalchemy.orm import Session

from hotel_reservation.controllers.schemas.room_schema import (
    RoomAvailabilityDatesSchema,
)
from hotel_reservation.exceptions.room_exceptions import NotFoundRoomError
from hotel_reservation.models.models import ReservationRulesCodes
from hotel_reservation.models.reservation_rules import ReservationRuleDAO
from hotel_reservation.models.room import RoomDAO

DEFAULT_MAX_ALLOWED_DAYS_TO_BOOK_IN_ADVANCE = 30
DEFAULT_MIN_ALLOWED_DAYS_TO_RESERVE = 1


class RoomServices:
    def __init__(self, session: Session):
        self.session = session
        self.room_model = RoomDAO(session)
        self.reservation_rules_dao = ReservationRuleDAO(session)

    def check_availability(self, room_id: int) -> RoomAvailabilityDatesSchema:
        (
            max_allowed_days_to_book_in_advance,
            min_allowed_days_to_reserve,
        ) = self.get_availability_related_rules()

        start_date = date.today() + timedelta(days=min_allowed_days_to_reserve)
        end_date = start_date + timedelta(days=max_allowed_days_to_book_in_advance)

        date_period_set = {
            start_date + timedelta(days=i)
            for i in range(max_allowed_days_to_book_in_advance)
        }

        room = self.room_model.get_by_id(room_id=room_id)
        if not room:
            raise NotFoundRoomError(room_id=room_id)

        booked_dates = self.room_model.get_room_booked_dates(
            start_date, end_date, room.id
        )
        booked_dates_set = {room_reservation.date for room_reservation in booked_dates}
        available_days = list(date_period_set.difference(booked_dates_set))
        available_days.sort()

        return RoomAvailabilityDatesSchema(
            room_number=room.number, available_dates=available_days
        )

    def get_availability_related_rules(self):
        rules = self.reservation_rules_dao.get_active_rules()
        max_allowed_days_to_book_in_advance = (
            DEFAULT_MAX_ALLOWED_DAYS_TO_BOOK_IN_ADVANCE
        )
        min_allowed_days_to_reserve = DEFAULT_MIN_ALLOWED_DAYS_TO_RESERVE
        for rule in rules:
            if (
                rule.code
                == ReservationRulesCodes.RESERVE_MAX_ALLOWED_BOOKING_IN_ADVANCE_DAYS
            ):
                max_allowed_days_to_book_in_advance = rule.value
            if (
                rule.code
                == ReservationRulesCodes.RESERVE_MIN_ALLOWED_DAYS_BETWEEN_BOOK_AND_RESERVATION_BEGIN
            ):
                min_allowed_days_to_reserve = rule.value
        return max_allowed_days_to_book_in_advance, min_allowed_days_to_reserve
