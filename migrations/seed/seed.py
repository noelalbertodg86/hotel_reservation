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

    reservation_rules = [
        ReservationRules(code=ReservationRulesCodes.RESERVE_MAX_ALLOWED_DAYS, value=3),
        ReservationRules(
            code=ReservationRulesCodes.RESERVE_MAX_ALLOWED_BOOKING_IN_ADVANCE_DAYS,
            value=30,
        ),
        ReservationRules(
            code=ReservationRulesCodes.RESERVE_MIN_ALLOWED_DAYS_BETWEEN_BOOK_AND_RESERVATION_BEGIN,
            value=1,
        ),
    ]

    session.add_all(reservation_rules)
    session.commit()


except Exception as seed_exception:
    print(f"Error during seed ingestion process: {seed_exception}")
