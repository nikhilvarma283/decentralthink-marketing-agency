"""Agent model for dental practices"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.database import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    practice_id = Column(UUID(as_uuid=True), ForeignKey("practices.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    cadence = Column(String, nullable=True)  # weekly, bi-weekly, monthly
    agent_type = Column(String, nullable=True)  # social_content, email_nurture, etc.
    prompt = Column(Text, nullable=True)
    status = Column(String, default="not_started")  # not_started, in_progress, completed, paused
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    practice = relationship("Practice", back_populates="agents")
    executions = relationship("Execution", back_populates="agent")

    def __repr__(self):
        return f"<Agent {self.name}>"
