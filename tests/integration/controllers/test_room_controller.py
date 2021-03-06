from datetime import date, timedelta, datetime

from fastapi import status, FastAPI
from fastapi.testclient import TestClient

from hotel_reservation.controllers.room_controlller import (
    router as room_router,
)
from hotel_reservation.database import get_db
from tests.integration.utils.reservation_test_utils import (
    build_object_reservation,
    create_reservation_for_testing_purposes,
)

app = FastAPI()
app.include_router(room_router)
client = TestClient(app)

app.dependency_overrides[get_db] = get_db


def test_should_return_room_availability_when_get_availability_method_is_called(
    faker, db_session
):
    room_id = 1
    start_day = date.today() + timedelta(days=10)
    second_day = start_day + timedelta(days=1)
    reservation_days = [start_day, second_day]
    reservation = build_object_reservation(faker, room_id, reservation_days, "")
    create_reservation_for_testing_purposes(db_session, reservation)
    max_allowed_days_to_reserve_in_advance = 30
    min_allowed_days_to_reserve = 1

    response = client.get(f"/v1/room/availability/{room_id}")

    assert response.status_code == status.HTTP_200_OK
    available_dates = [
        datetime.strptime(d, "%Y-%m-%d") for d in response.json()["available_dates"]
    ]
    available_dates.sort()
    assert len(available_dates) == max_allowed_days_to_reserve_in_advance - len(
        reservation_days
    )
    assert start_day not in available_dates
    assert second_day not in available_dates
    assert available_dates[0].date() == date.today() + timedelta(
        days=min_allowed_days_to_reserve
    )
    assert available_dates[-1].date() == date.today() + timedelta(
        days=max_allowed_days_to_reserve_in_advance
    )


def test_should_return_404_status_not_found_when_a_wrong_room_is_given():
    wrong_room_id = 99999

    error_response = client.get(f"/v1/room/availability/{wrong_room_id}")

    assert error_response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        error_response.json()["detail"] == f"Room with number:{wrong_room_id} Not Found"
    )
