from database import session_factory
from hotel_reservation.models.hotel import Hotel
from hotel_reservation.models.room import Room

try:
    session = session_factory()

    hotel = Hotel()
    hotel.address = "Cancun"
    hotel.name = "Unique Royal"
    hotel.rooms = Room(number=101)

    session.add(hotel)
    session.commit()


except Exception as seed_exception:
    print(f"Error during seed ingestion process: {seed_exception}")
