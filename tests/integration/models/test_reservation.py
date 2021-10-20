from datetime import date as Date, timedelta

import pytest

from hotel_reservation.exceptions.reservation_exceptions import (
    DuplicatedReservationError,
)
from hotel_reservation.models.models import Guest
from hotel_reservation.models.reservation import ReservationDAO
from tests.integration.utils.reservation_test_utils import build_object_reservation


def test_should_create_a_reservation_when_create_method_is_called(db_session, faker):
    reservation_data_model = ReservationDAO(db_session)
    observations = "Room with seaview"
    room_id = 1
    start_day = Date.today() + timedelta(days=10)
    second_day = start_day + timedelta(days=1)
    reservation_days = [start_day, second_day]

    reservation = build_object_reservation(
        faker, room_id, reservation_days, observations
    )
    created_reservation = reservation_data_model.create(reservation)

    assert created_reservation.id >= 1


def test_should_create_a_reservations_with_same_guest_in_distinct_dates_when_create_method_is_called(
    db_session, faker
):
    reservation_data_model = ReservationDAO(db_session)
    observations = "Room with seaview"
    room_id = 1
    start_day = Date.today() + timedelta(days=10)
    second_day = start_day + timedelta(days=1)
    reservation_days = [start_day, second_day]

    guest = Guest(
        identification=faker.pyint(),
        full_name=faker.name(),
        email=faker.email(),
        phone_number=faker.msisdn(),
    )

    reservation = build_object_reservation(
        faker,
        room_id,
        reservation_days,
        observations,
        guest=guest,
    )
    created_reservation = reservation_data_model.create(reservation)

    start_day = Date.today() + timedelta(days=20)
    second_day = start_day + timedelta(days=1)
    reservation_days = [start_day, second_day]

    new_reservation = build_object_reservation(
        faker,
        room_id,
        reservation_days,
        observations,
        guest=guest,
    )

    second_created_reservation = reservation_data_model.create(new_reservation)

    assert created_reservation.id >= 1
    assert second_created_reservation.id >= 1


def test_should_raise_an_error_when_duplicated_reservation_date_and_room_is_given(
    db_session, faker
):
    reservation_data_model = ReservationDAO(db_session)
    observations = "Room with seaview"
    room_id = 1
    start_day = Date.today() + timedelta(days=10)
    second_day = start_day + timedelta(days=1)
    reservation_days = [start_day, second_day]
    reservation = build_object_reservation(
        faker, room_id, reservation_days, observations
    )

    duplicated_reservation = build_object_reservation(
        faker, room_id, reservation_days, observations
    )

    created_reservation = reservation_data_model.create(reservation)

    assert created_reservation.id >= 1

    with pytest.raises(Exception) as duplicated_reservation_error:
        reservation_data_model.create(duplicated_reservation)
    assert isinstance(duplicated_reservation_error.value, DuplicatedReservationError)
