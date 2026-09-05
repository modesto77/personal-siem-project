from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- MODÈLE SQLALCHEMY (Base de données) ---
class LogEvent(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    source_host = Column(String, index=True)
    log_type = Column(String, index=True)
    severity = Column(String)
    event = Column(String)
    src_ip = Column(String, nullable=True)
    user = Column(String, nullable=True)
    raw_message = Column(String)

# --- SCHÉMA PYDANTIC (Validation des requêtes) ---
class LogCreate(BaseModel):
    timestamp: datetime
    source_host: str
    log_type: str
    severity: str
    event: str
    src_ip: Optional[str] = None
    user: Optional[str] = None
    raw_message: str

    class Config:
        from_attributes = True

# --- AJOUT : MODÈLE SQLALCHEMY (Table des alertes) ---
class AlertEvent(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    rule_name = Column(String)
    severity = Column(String)
    description = Column(String)
    source_ip = Column(String)        