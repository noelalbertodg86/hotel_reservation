from database import session_factory
from hotel_reservation.models.hotel import Hotel

try:
    session = session_factory()
    hotel = Hotel(session, "Unique Gran Hotel", "Cancun")
    hotel.save()

except Exception as seed_exception:
    print(f"Error during seed ingestion process: {seed_exception}")
