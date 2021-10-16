from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Session, relationship, declarative_base

Base = declarative_base()


class Hotel(Base):
    __tablename__ = "hotel"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(250))
    address = Column(String(250))

    rooms = relationship("Room", back_populates="hotel")

    def __init__(self, session: Session, name: str, address: str):
        self.session = session
        self.name = name
        self.address = address

    def save(self):
        self.session.add(self)
        self.session.commit()
