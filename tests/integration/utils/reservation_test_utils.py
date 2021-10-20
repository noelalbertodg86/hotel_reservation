from sqlalchemy.orm import Session

from hotel_reservation.models.models import Guest, RoomReservation, Reservation


def build_object_reservation(
    faker, room_id, reservation_dates, observations, guest: Guest = None
):
    if not guest:
        guest = Guest(
            identification=faker.pyint(),
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


def select_reservation_by_id(session: Session, reservation_id: int):
    reservation = (
        session.query(Reservation).filter(Reservation.id == reservation_id).first()
    )
    session.commit()
    return reservation


def build_reservation_from_payload(payload: dict):
    room_id = payload["room_id"]
    observations = payload["observations"]
    reservation_dates = payload["dates"]
    guest = Guest(**payload["guest"])
    return build_object_reservation(
        None, room_id, reservation_dates, observations, guest
    )
