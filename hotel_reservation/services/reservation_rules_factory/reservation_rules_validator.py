import abc

from hotel_reservation.models.models import Reservation, ReservationRules


class ReservationRuleValidator(abc.ABC):
    reservation_rule: ReservationRules

    def __init__(self, reservation_rule: ReservationRules):
        self.reservation_rule = reservation_rule

    @abc.abstractmethod
    def validate(self, reservation: Reservation) -> bool:
        raise NotImplementedError(
            "ReservationRulesFactory.validate_reservation method must be overwrite"
        )
