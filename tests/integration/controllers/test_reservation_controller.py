import copy
from datetime import date, timedelta

from fastapi import status, FastAPI
from fastapi.testclient import TestClient

from hotel_reservation.controllers.reservation_controller import (
    router as reservation_router,
)
from hotel_reservation.controllers.schemas.reservation_schemas import (
    ReservationUpdatedSchema,
)
from hotel_reservation.database import get_db
from tests.integration.utils.reservation_test_utils import (
    build_object_reservation,
    create_reservation_for_testing_purposes,
    select_reservation_by_id,
)

app = FastAPI()
app.include_router(reservation_router)
client = TestClient(app)

app.dependency_overrides[get_db] = get_db


def test_should_return_201_status_and_create_a_reservation_successfully(db_session):
    create_reservation_url = "/v1/reservation/"
    response = client.post(create_reservation_url, json=reservation_payload())

    assert response.status_code == status.HTTP_201_CREATED
    assert (
        select_reservation_by_id(
            db_session, int(response.json()["confirmation_number"])
        )
        is not None
    )


def test_should_return_400_status_bad_request_when_a_payload_with_wrong_email_is_given():
    payload_with_wrong_email = copy.deepcopy(reservation_payload())
    payload_with_wrong_email["guest"]["email"] = "noelgmail.com"
    create_reservation_url = "/v1/reservation/"
    error_response = client.post(create_reservation_url, json=payload_with_wrong_email)

    assert error_response.status_code == status.HTTP_400_BAD_REQUEST
    assert error_response.json()["detail"] == "Invalid email address"


def test_should_return_400_status_bad_request_when_a_paylod_with_wrong_phone_number_is_given():
    payload_with_wrong_phone = copy.deepcopy(reservation_payload())
    payload_with_wrong_phone["guest"]["phone_number"] = "12233445AX"
    create_reservation_url = "/v1/reservation/"
    error_response = client.post(create_reservation_url, json=payload_with_wrong_phone)

    assert error_response.status_code == status.HTTP_400_BAD_REQUEST
    assert error_response.json()["detail"] == "Invalid phone number"


def test_should_return_409_status_conflict_when_a_reservation_is_duplicated(faker):
    create_reservation_url = "/v1/reservation/"
    new_guest_reservation = copy.deepcopy(reservation_payload())
    guest_1 = {
        "identification": faker.pyint(),
        "full_name": faker.name(),
        "email": faker.email(),
        "phone_number": faker.msisdn(),
    }

    new_guest_reservation["guest"] = guest_1

    response = client.post(create_reservation_url, json=new_guest_reservation)

    assert response.status_code == status.HTTP_201_CREATED
    assert int(response.json()["confirmation_number"]) >= 0

    guest_2 = {
        "identification": faker.pyint(),
        "full_name": faker.name(),
        "email": faker.email(),
        "phone_number": faker.msisdn(),
    }

    new_guest_reservation["guest"] = guest_2

    error_response = client.post(create_reservation_url, json=new_guest_reservation)

    assert error_response.status_code == status.HTTP_409_CONFLICT
    expected_error_message = (
        f"Duplicated reservation. Room: 1, Dates: {reservation_payload()['dates']}"
    )
    assert error_response.json()["detail"] == expected_error_message


def test_should_update_a_reservation_and_return_200_when_update_reservation_endpoint_is_called(
    faker, db_session
):
    room_id = 1
    start_day = date.today() + timedelta(days=10)
    second_day = start_day + timedelta(days=1)
    reservation_days = [start_day, second_day]
    reservation = build_object_reservation(faker, room_id, reservation_days, "")
    reservation = create_reservation_for_testing_purposes(db_session, reservation)

    create_reservation_url = f"/v1/reservation/{reservation.id}"
    response = client.put(create_reservation_url, json=reservation_payload())

    assert response.status_code == status.HTTP_200_OK
    updated_reservation = select_reservation_by_id(
        session=db_session, reservation_id=reservation.id
    )
    expected_response = ReservationUpdatedSchema.build_from_reservation_model(
        updated_reservation
    ).dict()
    expected_response["dates"] = list(map(str, expected_response["dates"]))
    assert response.json() == expected_response


def test_should_delete_a_reservation_and_return_200_when_delete_reservation_endpoint_is_called(
    faker, db_session
):
    room_id = 1
    start_day = date.today() + timedelta(days=10)
    second_day = start_day + timedelta(days=1)
    reservation_days = [start_day, second_day]
    reservation = build_object_reservation(faker, room_id, reservation_days, "")
    reservation = create_reservation_for_testing_purposes(db_session, reservation)

    delete_reservation_url = f"/v1/reservation/{reservation.id}"
    response = client.delete(delete_reservation_url)

    assert response.status_code == status.HTTP_200_OK
    assert not select_reservation_by_id(db_session, reservation.id)


def test_should_raise_not_found_error_when_delete_reservation_endpoint_is_called_with_wrong_confirmation():
    wrong_reservation_confirmation = 9999

    delete_reservation_url = f"/v1/reservation/{wrong_reservation_confirmation}"
    response = client.delete(delete_reservation_url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    msg = f"Reservation with confirmation number:{wrong_reservation_confirmation} Not Found"
    assert response.json()["detail"] == msg


def test_should_raise_409_validation_error_when_a_reservation_with_more_than_3_days_is_send():
    start_day = date.today() + timedelta(days=10)
    reservation_with_5_days = [str(start_day + timedelta(days=i)) for i in range(5)]
    payload = reservation_payload()
    payload["dates"] = reservation_with_5_days

    create_reservation_url = "/v1/reservation/"
    error_response = client.post(create_reservation_url, json=payload)

    assert error_response.status_code == status.HTTP_409_CONFLICT
    msg = "Max allowed reservation stay is 3 days"
    assert error_response.json()["detail"] == msg


def test_should_raise_409_validation_error_when_a_reservation_with_more_than_30_days_in_advance_is_send():
    start_day = date.today() + timedelta(days=31)
    reservation_days = [str(start_day + timedelta(days=i)) for i in range(3)]
    payload = reservation_payload()
    payload["dates"] = reservation_days

    create_reservation_url = "/v1/reservation/"
    error_response = client.post(create_reservation_url, json=payload)

    assert error_response.status_code == status.HTTP_409_CONFLICT
    msg = "Reservations must be made until 30 days in advance"
    assert error_response.json()["detail"] == msg


def test_should_raise_409_validation_error_when_a_reservation_for_today_is_send():
    start_day = date.today()
    reservation_days = [str(start_day + timedelta(days=i)) for i in range(3)]
    payload = reservation_payload()
    payload["dates"] = reservation_days

    create_reservation_url = "/v1/reservation/"
    error_response = client.post(create_reservation_url, json=payload)

    msg = "Reservations must be made with at least 1 day in advance"
    assert error_response.status_code == status.HTTP_409_CONFLICT
    assert error_response.json()["detail"] == msg


def reservation_payload():
    return {
        "dates": [
            f"{date.today() + timedelta(days=15)}",
            f"{date.today() + timedelta(days=16)}",
            f"{date.today() + timedelta(days=17)}",
        ],
        "guest": {
            "identification": "13131313",
            "full_name": "Noel Diaz",
            "email": "noel@gmail.com",
            "phone_number": "1234567890",
        },
        "room_id": 1,
        "observations": "Room with seaview",
    }
