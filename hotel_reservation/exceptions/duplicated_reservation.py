from hotel_reservation.models.models import Reservation


class DuplicatedReservationError(Exception):
    def __init__(self, room, dates):
        msg = f"Duplicated reservation. Room: {room}, Dates: {dates}"
        super().__init__(msg)
