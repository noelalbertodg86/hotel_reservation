from typing import Optional, List

from sqlalchemy.orm import Session

from hotel_reservation.models.models import ReservationRules


class ReservationRuleDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_active_rules(self) -> Optional[List[ReservationRules]]:
        return (
            self.session.query(ReservationRules)
            .filter(ReservationRules.active == True)
            .all()
        )

    def create(self, reservation_rules: ReservationRules):
        try:
            self.session.add(reservation_rules)
            self.session.commit()
        except Exception as rules_error:
            self.session.rollback()
            raise rules_error

    def deactivate(self, reservation_rules: ReservationRules):
        try:
            reservation_rules.active = False
            self.session.commit()
        except Exception as deactivate_error:
            self.session.rollback()
            raise deactivate_error
