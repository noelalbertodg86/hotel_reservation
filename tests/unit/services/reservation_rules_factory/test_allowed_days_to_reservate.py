import pytest

from hotel_reservation.exceptions.reservation_rules_exceptions import (
    InvalidValidatorClass,
)
from hotel_reservation.models.models import ReservationRules, ReservationRulesCodes
from hotel_reservation.services.reservation_rules_factory.allowed_days_to_reservate import (
    MinAllowedDaysToReservate,
)


def test_should_raise_invalid_validator_class_when_wrong_validator_is_created():
    wrong_reservation_rule = ReservationRules(
        code=ReservationRulesCodes.RESERVE_MAX_ALLOWED_DAYS, value=3
    )
    with pytest.raises(InvalidValidatorClass) as invalid_validator:
        MinAllowedDaysToReservate(wrong_reservation_rule)

    expected_code = (
        ReservationRulesCodes.RESERVE_MIN_ALLOWED_DAYS_BETWEEN_BOOK_AND_RESERVATION_BEGIN
    )
    msg = f"AllowedDaysForBookingInAdvance expected code: {expected_code} and got: {wrong_reservation_rule.code}"
    assert invalid_validator.value.detail == msg


def test_should_create_validator_successfully_when_the_right_rules_is_given():
    right_reservation_rule = ReservationRules(
        code=ReservationRulesCodes.RESERVE_MIN_ALLOWED_DAYS_BETWEEN_BOOK_AND_RESERVATION_BEGIN,
        value=1,
    )

    created_validator = MinAllowedDaysToReservate(right_reservation_rule)

    assert isinstance(created_validator, MinAllowedDaysToReservate)
    assert created_validator.reservation_rule == right_reservation_rule
