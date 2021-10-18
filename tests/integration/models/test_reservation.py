from datetime import date, timedelta

import pytest

from hotel_reservation.exceptions.duplicated_reservation import (
    DuplicatedReservationError,
)
from hotel_reservation.models.models import Guest
from hotel_reservation.models.reservation import ReservationDAO


def test_should_create_a_reservation_when_create_method_is_called(db_session, faker):
    reservation_data_model = ReservationDAO(db_session)
    today = date.today()
    tomorrow = today + timedelta(days=1)
    reservation_dates = [today, tomorrow]
    observations = "Room with seaview"
    room_id = 1
    guest = Guest(
        id=faker.text(10),
        full_name=faker.name(),
        email=faker.email(),
        phone_number=faker.msisdn(),
    )
    created_reservation = reservation_data_model.create(
        reservation_dates=reservation_dates,
        observations=observations,
        room_id=room_id,
        guest=guest,
    )

    assert created_reservation.id >= 1


def test_should_raise_an_error_when_duplicated_reservation_date_and_room_is_given(
    db_session, faker
):
    reservation_data_model = ReservationDAO(db_session)
    today = date.today()
    tomorrow = today + timedelta(days=1)
    reservation_dates = [today, tomorrow]
    observations = "Room with seaview"
    room_id = 1
    guest = Guest(
        id=faker.text(10),
        full_name=faker.name(),
        email=faker.email(),
        phone_number=faker.msisdn(),
    )

    created_reservation = reservation_data_model.create(
        reservation_dates=reservation_dates,
        observations=observations,
        room_id=room_id,
        guest=guest,
    )

    assert created_reservation.id >= 1

    with pytest.raises(Exception) as duplicated_reservation_error:
        reservation_data_model.create(
            reservation_dates=reservation_dates,
            observations=observations,
            room_id=room_id,
            guest=guest,
        )
    import pdb

    pdb.set_trace()
    assert isinstance(duplicated_reservation_error.value, DuplicatedReservationError)
