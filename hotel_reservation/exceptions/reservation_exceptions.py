from fastapi import HTTPException, status

from hotel_reservation.models.models import Reservation


class DuplicatedReservationError(HTTPException):
    def __init__(self, reservation: Reservation):
        msg = (
            f"Duplicated reservation. Room: {reservation.room_reservations[0].room_id}, "
            f"Dates: {reservation.get_dates_to_str()}"
        )
        HTTPException.__init__(self, status_code=status.HTTP_409_CONFLICT, detail=msg)


class NotFoundReservationError(HTTPException):
    def __init__(self, reservation_confirmation_number: int):
        msg = f"Reservation with confirmation number:{reservation_confirmation_number} Not Found"
        HTTPException.__init__(self, status_code=status.HTTP_404_NOT_FOUND, detail=msg)
