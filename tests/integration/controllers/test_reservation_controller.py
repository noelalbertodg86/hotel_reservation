import copy
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from hotel_reservation.controllers.reservation_controller import (
    router as reservation_router,
)
from hotel_reservation.models.models import Reservation
from tests.integration.utils.reservation_test_utils import (
    build_object_reservation,
    create_reservation_for_testing_purposes,
)

client = TestClient(reservation_router)


def test_should_return_201_status_and_create_a_reservation_successfully():
    create_reservation_url = "/v1/reservation/"
    response = client.post(create_reservation_url, json=CREATE_RESERVATION_PAYLOAD)

    assert response.status_code == status.HTTP_201_CREATED
    assert int(response.json()["confirmation_number"]) >= 0


def test_should_return_400_status_bad_request_when_a_paylod_with_wrong_email_is_given():
    payload_with_wrong_email = copy.deepcopy(CREATE_RESERVATION_PAYLOAD)
    payload_with_wrong_email["guest"]["email"] = "noelgmail.com"
    create_reservation_url = "/v1/reservation/"
    with pytest.raises(HTTPException) as wrong_email_error:
        client.post(create_reservation_url, json=payload_with_wrong_email)

    assert wrong_email_error.value.status_code == status.HTTP_400_BAD_REQUEST
    assert wrong_email_error.value.detail == "Invalid email address"


def test_should_return_400_status_bad_request_when_a_paylod_with_wrong_phone_number_is_given():
    payload_with_wrong_phone = copy.deepcopy(CREATE_RESERVATION_PAYLOAD)
    payload_with_wrong_phone["guest"]["phone_number"] = "12233445AX"
    create_reservation_url = "/v1/reservation/"
    with pytest.raises(HTTPException) as wrong_phone_error:
        client.post(create_reservation_url, json=payload_with_wrong_phone)

    assert wrong_phone_error.value.status_code == status.HTTP_400_BAD_REQUEST
    assert wrong_phone_error.value.detail == "Invalid phone number"


def test_should_return_409_status_conflict_when_a_reservation_is_duplicated(faker):
    create_reservation_url = "/v1/reservation/"
    new_guest_reservation = copy.deepcopy(CREATE_RESERVATION_PAYLOAD)
    guest_1 = {
        "id": faker.pyint(),
        "full_name": faker.name(),
        "email": faker.email(),
        "phone_number": faker.msisdn(),
    }

    new_guest_reservation["guest"] = guest_1

    response = client.post(create_reservation_url, json=new_guest_reservation)

    assert response.status_code == status.HTTP_201_CREATED
    assert int(response.json()["confirmation_number"]) >= 0

    guest_2 = {
        "id": faker.pyint(),
        "full_name": faker.name(),
        "email": faker.email(),
        "phone_number": faker.msisdn(),
    }

    new_guest_reservation["guest"] = guest_2

    with pytest.raises(HTTPException) as duplicated_reservation:
        client.post(create_reservation_url, json=new_guest_reservation)

    assert duplicated_reservation.value.status_code == status.HTTP_409_CONFLICT
    expected_error_message = (
        f"Duplicated reservation. Room: 1, Dates: {CREATE_RESERVATION_PAYLOAD['dates']}"
    )
    assert duplicated_reservation.value.detail == expected_error_message


def test_should_update_a_reservation_and_return_200_when_update_reservation_endpoint_is_called(
    faker, db_session
):
    room_id = 1
    start_day = date.today() + timedelta(days=10)
    second_day = start_day + timedelta(days=1)
    reservation_days = [start_day, second_day]
    reservation = build_object_reservation(faker, room_id, reservation_days, "")
    reservation = create_reservation_for_testing_purposes(db_session, reservation)

    existing_reservation_confirmation_number = reservation.id

    create_reservation_url = (
        f"/v1/reservation/{existing_reservation_confirmation_number}"
    )
    response = client.put(create_reservation_url, json=CREATE_RESERVATION_PAYLOAD)

    assert response.status_code == status.HTTP_200_OK


CREATE_RESERVATION_PAYLOAD = {
    "dates": [
        f"{date.today() + timedelta(days=15)}",
        f"{date.today() + timedelta(days=16)}",
        f"{date.today() + timedelta(days=17)}",
    ],
    "guest": {
        "id": "13131313",
        "full_name": "Noel Diaz",
        "email": "noel@gmail.com",
        "phone_number": "1234567890",
    },
    "room_id": 1,
    "observations": "Room with seaview",
}