from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Hotel(Base):
    __tablename__ = "hotel"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(250))
    address = Column(String(250))
    rooms = relationship("Room", back_populates="hotel")
