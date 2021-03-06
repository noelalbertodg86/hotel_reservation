from datetime import date

from hotel_reservation.exceptions.reservation_rules_exceptions import (
    InvalidValidatorClass,
    ReservationDaysToReservateError,
)
from hotel_reservation.models.models import (
    Reservation,
    ReservationRules,
    ReservationRulesCodes,
)
from hotel_reservation.services.reservation_rules_factory.reservation_rules_validator import (
    ReservationRuleValidator,
)


class MinAllowedDaysToReservate(ReservationRuleValidator):
    def __init__(self, reservation_rule: ReservationRules):
        expected_code = (
            ReservationRulesCodes.RESERVE_MIN_ALLOWED_DAYS_BETWEEN_BOOK_AND_RESERVATION_BEGIN
        )
        if reservation_rule.code != expected_code:
            raise InvalidValidatorClass(
                f"AllowedDaysForBookingInAdvance expected code: {expected_code} and got: {reservation_rule.code}"
            )
        super().__init__(reservation_rule)

    def validate(self, reservation: Reservation) -> bool:
        today = date.today()
        reservation_start_day = min(
            [
                room_reservation.date
                for room_reservation in reservation.room_reservations
            ]
        )
        if (reservation_start_day - today).days < self.reservation_rule.value:
            raise ReservationDaysToReservateError(self.reservation_rule)
        return True
