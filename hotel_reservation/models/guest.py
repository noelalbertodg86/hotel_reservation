from typing import Optional

from sqlalchemy.orm import Session

from hotel_reservation.models.model_base_dao import ModelBaseDAO
from hotel_reservation.models.models import Guest


class GuestDAO(ModelBaseDAO):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_by_id(self, guest_id: str) -> Optional[Guest]:
        return (
            self.session.query(Guest).filter(Guest.identification == guest_id).first()
        )
