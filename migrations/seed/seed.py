from database import session_factory
from hotel_reservation.models.models import *

try:
    session = session_factory()
    hotel = Hotel(name="Unique Royal", address="Cancun")
    room = Room(number=101)
    hotel.rooms.append(room)
    guest = Guest(
        id="123456789",
        full_name="Jhon Snow",
        email="jhon@winterfall.com",
        phone_number=9988776655,
    )

    session.add(hotel)
    session.add(guest)
    session.commit()


except Exception as seed_exception:
    print(f"Error during seed ingestion process: {seed_exception}")
