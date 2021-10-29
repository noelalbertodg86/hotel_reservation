from typing import Optional, List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from hotel_reservation.models.model_base_dao import ModelBaseDAO
from hotel_reservation.models.models import ReservationRules, ReservationRulesCodes


class ReservationRuleDAO(ModelBaseDAO):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_active_rules(self) -> Optional[List[ReservationRules]]:
        return (
            self.session.query(ReservationRules)
            .filter(ReservationRules.active == True)
            .all()
        )

    def get_rules_by_code(
        self, code: ReservationRulesCodes
    ) -> Optional[ReservationRules]:
        return (
            self.session.query(ReservationRules)
            .filter(
                and_(
                    ReservationRules.code == code.value, ReservationRules.active == True
                )
            )
            .first()
        )

    def get_by_id(self, model_id: int):
        pass
