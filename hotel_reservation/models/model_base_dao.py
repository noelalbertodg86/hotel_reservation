from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session

from hotel_reservation.models.models import Base


class ModelBaseDAO(ABC):
    def __init__(self, session: Session):
        self.session = session

    def create(self, model: Base) -> Base:
        try:
            self.session.add(model)
            self.session.commit()
            return model
        except Exception as unexpected_error:
            self.session.rollback()
            raise unexpected_error

    def update(self, model: Base) -> Base:
        try:
            self.session.merge(model)
            self.session.commit()
            return model
        except Exception as error:
            self.session.rollback()
            raise error

    @abstractmethod
    def get_by_id(self, model_id: int) -> Optional[Base]:
        return NotImplementedError("Method must be implemented in child class")

    def delete(self, model: Base) -> Base:
        try:
            self.session.delete(model)
            self.session.commit()
            return model
        except Exception as deleted_error:
            self.session.rollback()
            raise deleted_error
