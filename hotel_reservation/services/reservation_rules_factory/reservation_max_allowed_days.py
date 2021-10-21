from hotel_reservation.exceptions.reservation_rules_exceptions import (
    InvalidValidatorClass,
    ReservationMaxAllowedDaysError,
)
from hotel_reservation.models.models import (
    Reservation,
    ReservationRules,
    ReservationRulesCodes,
)
from hotel_reservation.services.reservation_rules_factory.reservation_rules_validator import (
    ReservationRuleValidator,
)


class ReservationMaxAllowedDays(ReservationRuleValidator):
    def __init__(self, reservation_rule: ReservationRules):
        expected_code = ReservationRulesCodes.RESERVE_MAX_ALLOWED_DAYS
        if reservation_rule.code != expected_code:
            raise InvalidValidatorClass(
                f"ReservationMaxAllowedDays expected code: {expected_code} and got: {reservation_rule.code}"
            )
        super().__init__(reservation_rule)

    def validate(self, reservation: Reservation) -> bool:
        reservation_len = len(reservation.room_reservations)
        if reservation_len > self.reservation_rule.value:
            raise ReservationMaxAllowedDaysError(self.reservation_rule)
        return True
