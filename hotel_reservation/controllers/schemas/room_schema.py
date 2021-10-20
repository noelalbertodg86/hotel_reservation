from datetime import date
from typing import List

from pydantic import BaseModel


class RoomBaseSchema(BaseModel):
    room_number: int


class RoomAvailabilityDatesSchema(RoomBaseSchema):
    message: str = f"Room availability"
    available_dates: List[date]
