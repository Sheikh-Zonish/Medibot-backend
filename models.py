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

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    generic_info = Column(String, nullable=False)
    condition = Column(String, nullable=False)
    color_hex = Column(String, nullable=False)
    is_suggested = Column(Integer, default=0)

class SafetyCheckLog(Base):
    __tablename__ = "safety_check_logs"

    id = Column(Integer, primary_key=True)
    medication_name = Column(String)
    severity = Column(String)
    message = Column(String)
    checked_at = Column(DateTime, default=datetime.utcnow)
