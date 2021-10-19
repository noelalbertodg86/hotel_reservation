from typing import List

from hotel_reservation.models.models import ReservationRules, ReservationRulesCodes
from hotel_reservation.services.reservation_rules_factory.allowed_days_for_booking_in_advance import (
    AllowedDaysForBookingInAdvance,
)
from hotel_reservation.services.reservation_rules_factory.allowed_days_to_reservate import (
    MinAllowedDaysToReservate,
)
from hotel_reservation.services.reservation_rules_factory.reservation_max_allowed_days import (
    ReservationMaxAllowedDays,
)
from hotel_reservation.services.reservation_rules_factory.reservation_rules_validator import (
    ReservationRuleValidator,
)


class ReservationRulesFactory:
    def __init__(self, reservation_rules: List[ReservationRules]):
        self.reservation_rules = reservation_rules

    def get_validators(self) -> List[ReservationRuleValidator]:
        validators = []
        for rule in self.reservation_rules:
            if rule.code == ReservationRulesCodes.RESERVE_MAX_ALLOWED_DAYS:
                validators.append(ReservationMaxAllowedDays(rule))
            elif (
                rule.code
                == ReservationRulesCodes.RESERVE_MAX_ALLOWED_BOOKING_IN_ADVANCE_DAYS
            ):
                validators.append(AllowedDaysForBookingInAdvance(rule))
            elif (
                rule.code
                == ReservationRulesCodes.RESERVE_MIN_ALLOWED_DAYS_BETWEEN_BOOK_AND_RESERVATION_BEGIN
            ):
                validators.append(MinAllowedDaysToReservate(rule))
            else:
                raise NotImplementedError(
                    f"Not implemented reservation rule: {rule.code}"
                )
        return validators
