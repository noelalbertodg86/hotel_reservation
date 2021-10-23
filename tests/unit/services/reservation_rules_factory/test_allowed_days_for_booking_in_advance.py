import pytest

from hotel_reservation.exceptions.reservation_rules_exceptions import (
    InvalidValidatorClass,
)
from hotel_reservation.models.models import ReservationRules, ReservationRulesCodes
from hotel_reservation.services.reservation_rules_factory.allowed_days_for_booking_in_advance import (
    AllowedDaysForBookingInAdvance,
)


def test_should_raise_invalid_validator_class_when_wrong_validator_is_created():
    wrong_reservation_rule = ReservationRules(
        code=ReservationRulesCodes.RESERVE_MAX_ALLOWED_DAYS, value=3
    )
    with pytest.raises(InvalidValidatorClass) as invalid_validator:
        AllowedDaysForBookingInAdvance(wrong_reservation_rule)

    expected_code = ReservationRulesCodes.RESERVE_MAX_ALLOWED_BOOKING_IN_ADVANCE_DAYS
    msg = f"AllowedDaysForBookingInAdvance expected code: {expected_code} and got: {wrong_reservation_rule.code}"
    assert invalid_validator.value.detail == msg


def test_should_create_validator_successfully_when_the_right_rules_is_given():
    right_reservation_rule = ReservationRules(
        code=ReservationRulesCodes.RESERVE_MAX_ALLOWED_BOOKING_IN_ADVANCE_DAYS, value=30
    )

    created_validator = AllowedDaysForBookingInAdvance(right_reservation_rule)

    assert isinstance(created_validator, AllowedDaysForBookingInAdvance)
    assert created_validator.reservation_rule == right_reservation_rule
