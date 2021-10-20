from typing import Optional

from sqlalchemy.orm import Session

from hotel_reservation.models.models import Guest


class GuestDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_guest_by_id(self, guest_id: str) -> Optional[Guest]:
        return (
            self.session.query(Guest).filter(Guest.identification == guest_id).first()
        )
