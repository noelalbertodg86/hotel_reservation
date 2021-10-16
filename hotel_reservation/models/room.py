from sqlalchemy.orm import Session

from hotel_reservation.models.models import Room


class RoomDAO:
    def __init__(self, session: Session):
        self.session = session

    def create(self, number: int, hotel_id: int):
        try:
            room = Room(number=number, hotel_id=hotel_id)
            self.session.add(room)
            self.session.commit()
        except Exception as exception:
            self.session.rollback()
            raise exception
