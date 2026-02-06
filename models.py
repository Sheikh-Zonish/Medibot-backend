from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    medication_name = Column(String)
    time = Column(String)

class DoseLog(Base):
    __tablename__ = "dose_logs"

    id = Column(Integer, primary_key=True)
    medication_name = Column(String)
    taken_at = Column(DateTime, default=datetime.utcnow)

