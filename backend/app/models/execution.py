"""Execution/Task model for agent actions"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
from datetime import datetime

from app.database import Base


class Execution(Base):
    __tablename__ = "executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    action_type = Column(String, nullable=False)  # twitter_post, linkedin_post, email, manual
    content = Column(Text, nullable=False)
    status = Column(String, default="pending")  # pending, approved, posted, failed
    result = Column(JSON, nullable=True)  # success/failure details
    executed_date = Column(DateTime, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    agent = relationship("Agent", back_populates="executions")

    def __repr__(self):
        return f"<Execution {self.id}>"
