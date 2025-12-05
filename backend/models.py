from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from db import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    severity = Column(String(16), default="info", nullable=False)
    source = Column(String(64), nullable=False)
    category = Column(String(64), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(16), nullable=False)
    source = Column(String(64), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
