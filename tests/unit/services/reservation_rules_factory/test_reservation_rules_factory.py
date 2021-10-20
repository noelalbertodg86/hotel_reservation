from datetime import date, timedelta
from fastapi import status
import pytest

from hotel_reservation.exceptions.reservation_rules_exceptions import (
    InvalidReservationStayError,
    UnauthorizedDaysRangeForBooking,
)
from hotel_reservation.models.models import (
    ReservationRules,
    ReservationRulesCodes,
    Guest,
)
from hotel_reservation.services.reservation_rules_factory.allowed_days_for_booking_in_advance import (
    AllowedDaysForBookingInAdvance,
)
from hotel_reservation.services.reservation_rules_factory.allowed_days_to_reservate import (
    MinAllowedDaysToReservate,
)
from hotel_reservation.services.reservation_rules_factory.reservation_max_allowed_days import (
    ReservationMaxAllowedDays,
)
from hotel_reservation.services.reservation_rules_factory.reservation_rules_factory import (
    ReservationRulesFactory,
)
from tests.integration.utils.reservation_test_utils import build_object_reservation


def test_should_create_one_rule_validator_per_rule_given():
    reservation_rules_factory = ReservationRulesFactory(build_reservation_rules())
    validators = reservation_rules_factory.get_validators()

    assert len(validators) == 3
    assert isinstance(validators[0], ReservationMaxAllowedDays)
    assert isinstance(validators[1], AllowedDaysForBookingInAdvance)
    assert isinstance(validators[2], MinAllowedDaysToReservate)


def test_validators_should_raise_error_when_reservation_with_more_than_3_days_is_given():
    observations = "Room with seaview"
    room_id = 1
    start_day = date.today() + timedelta(days=10)
    reservation_days = [start_day + timedelta(days=i) for i in range(5)]
    guest = Guest(
        identification="1010101010",
        full_name="John Snow",
        email="a@a.com",
        phone_number="12345678",
    )
    reservation = build_object_reservation(
        None, room_id, reservation_days, observations, guest=guest
    )
    validators = ReservationRulesFactory(build_reservation_rules()).get_validators()

    with pytest.raises(Exception) as validator_exception:
        [validator.validate(reservation) for validator in validators]

    assert isinstance(validator_exception.value, InvalidReservationStayError)
    assert validator_exception.value.status_code == status.HTTP_409_CONFLICT
    assert validator_exception.value.detail == "Max allowed reservation stay is 3 days"


def test_validators_should_raise_error_when_reservation_is_booked_for_the_same_day():
    observations = "Room with seaview"
    room_id = 1
    start_day = date.today()
    reservation_days = [start_day + timedelta(days=i) for i in range(3)]
    guest = Guest(
        identification="1010101010",
        full_name="John Snow",
        email="a@a.com",
        phone_number="12345678",
    )
    reservation = build_object_reservation(
        None, room_id, reservation_days, observations, guest=guest
    )
    validators = ReservationRulesFactory(build_reservation_rules()).get_validators()

    with pytest.raises(Exception) as validator_exception:
        [validator.validate(reservation) for validator in validators]

    assert isinstance(validator_exception.value, UnauthorizedDaysRangeForBooking)
    assert validator_exception.value.status_code == status.HTTP_409_CONFLICT
    assert (
        validator_exception.value.detail
        == "Reservations need to be made with at least 1 days in advance"
    )


def test_validators_should_raise_error_when_reservation_is_booked_for_more_than_30_days_in_advance():
    observations = "Room with seaview"
    room_id = 1
    start_day = date.today() + timedelta(days=31)
    reservation_days = [start_day + timedelta(days=i) for i in range(3)]
    guest = Guest(
        identification="1010101010",
        full_name="John Snow",
        email="a@a.com",
        phone_number="12345678",
    )
    reservation = build_object_reservation(
        None, room_id, reservation_days, observations, guest=guest
    )
    validators = ReservationRulesFactory(build_reservation_rules()).get_validators()

    with pytest.raises(Exception) as validator_exception:
        [validator.validate(reservation) for validator in validators]

    assert isinstance(validator_exception.value, UnauthorizedDaysRangeForBooking)
    assert validator_exception.value.status_code == status.HTTP_409_CONFLICT
    assert (
        validator_exception.value.detail
        == "Reservations need to be made with at least 30 days in advance"
    )


def build_reservation_rules():
    max_stay_days = ReservationRules(
        code=ReservationRulesCodes.RESERVE_MAX_ALLOWED_DAYS, value=3
    )
    allowed_days_for_booking_in_advance = ReservationRules(
        code=ReservationRulesCodes.RESERVE_MAX_ALLOWED_BOOKING_IN_ADVANCE_DAYS, value=30
    )
    allowed_days_to_reservate = ReservationRules(
        code=ReservationRulesCodes.RESERVE_MIN_ALLOWED_DAYS_BETWEEN_BOOK_AND_RESERVATION_BEGIN,
        value=1,
    )
    return [
        max_stay_days,
        allowed_days_for_booking_in_advance,
        allowed_days_to_reservate,
    ]
