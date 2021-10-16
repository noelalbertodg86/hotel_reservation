from typing import List, Optional

from sqlalchemy.orm import Session

from hotel_reservation.models.models import Room, Hotel


class HotelDAO:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, address: str, rooms: Optional[List[Room]]):
        hotel = Hotel(name=name, address=address, rooms=rooms)
        self.session.add(hotel)
        self.session.commit()
