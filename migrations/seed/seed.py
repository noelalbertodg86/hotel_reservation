from database import session_factory
from hotel_reservation.models.models import Hotel, Room

try:
    session = session_factory()

    hotel = Hotel(name="Unique Royal", address="Cancun")
    hotel.rooms.append(Room(number=101))

    session.add(hotel)
    session.commit()


except Exception as seed_exception:
    print(f"Error during seed ingestion process: {seed_exception}")
