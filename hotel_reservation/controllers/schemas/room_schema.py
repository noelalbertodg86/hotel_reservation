from datetime import date
from typing import List

from pydantic import BaseModel


class RoomBaseSchema(BaseModel):
    room_number: int


class RoomAvailabilityDatesSchema(RoomBaseSchema):
    message: str = "Room availability in the next 30 days"
    available_dates: List[date]
