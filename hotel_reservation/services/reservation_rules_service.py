from typing import List

from sqlalchemy.orm import Session

from hotel_reservation.models.reservation_rules import ReservationRuleDAO
from hotel_reservation.services.reservation_rules_factory.reservation_rules_factory import (
    ReservationRulesFactory,
)
from hotel_reservation.services.reservation_rules_factory.reservation_rules_validator import (
    ReservationRuleValidator,
)


class ReservationRulesService:
    def __init__(self, session: Session):
        self.session = session
        self.reservation_rules_dao = ReservationRuleDAO(session)

    def get_rules_validators(self) -> List[ReservationRuleValidator]:
        active_reservation_rules = self.reservation_rules_dao.get_active_rules()
        return ReservationRulesFactory(active_reservation_rules).get_validators()
