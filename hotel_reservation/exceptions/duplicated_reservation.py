from typing import List

from fastapi import HTTPException, status
from datetime import date as Date


class DuplicatedReservationError(HTTPException):
    def __init__(self, room, dates: List[Date]):
        formatted_dates = list(map(str, dates))
        msg = f"Duplicated reservation. Room: {room}, Dates: {formatted_dates}"
        HTTPException.__init__(self, status_code=status.HTTP_409_CONFLICT, detail=msg)
