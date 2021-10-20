from fastapi import HTTPException, status

from hotel_reservation.models.models import ReservationRules


class InvalidReservationStayError(HTTPException):
    def __init__(self, reservation_rule: ReservationRules):
        msg = f"Max allowed reservation stay is {reservation_rule.value} days"
        HTTPException.__init__(self, status_code=status.HTTP_409_CONFLICT, detail=msg)


class InvalidValidatorClass(HTTPException):
    def __init__(self, msg: str):
        HTTPException.__init__(self, status_code=status.HTTP_409_CONFLICT, detail=msg)


class UnauthorizedDaysRangeForBooking(HTTPException):
    def __init__(self, reservation_rule: ReservationRules):
        msg = f"Reservations need to be made with at least {reservation_rule.value} days in advance"
        HTTPException.__init__(self, status_code=status.HTTP_409_CONFLICT, detail=msg)
