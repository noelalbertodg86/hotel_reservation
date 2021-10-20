import pytest
from faker import Faker

from hotel_reservation.database import session_factory
from hotel_reservation.models.models import Reservation, RoomReservation, Guest


@pytest.fixture(scope="session")
def db_session():
    local_session = session_factory()
    yield local_session
    local_session.close()


@pytest.fixture(scope="session")
def faker():
    return Faker()


@pytest.fixture(autouse=True)
def clean_test_data():
    yield
    local_session = session_factory()
    local_session.query(RoomReservation).delete()
    local_session.query(Reservation).delete()
    local_session.query(Guest).delete()
    local_session.commit()
