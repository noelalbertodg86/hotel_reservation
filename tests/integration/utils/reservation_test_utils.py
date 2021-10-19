from sqlalchemy.orm import Session

from hotel_reservation.models.models import Guest, RoomReservation, Reservation


def build_object_reservation(
    faker, room_id, reservation_dates, observations, guest: Guest = None
):
    if not guest:
        guest = Guest(
            id=faker.pyint(),
            full_name=faker.name(),
            email=faker.email(),
            phone_number=faker.msisdn(),
        )

    room_reservations = [
        RoomReservation(date=date, room_id=room_id) for date in reservation_dates
    ]

    return Reservation(
        observations=observations,
        room_reservations=room_reservations,
        guest=guest,
    )


def create_reservation_for_testing_purposes(session: Session, reservation: Reservation):
    session.add(reservation)
    session.commit()
    return reservation
