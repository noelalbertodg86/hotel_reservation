from sqlalchemy import Column, Integer, Date, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(Date, nullable=False)
    guests = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())