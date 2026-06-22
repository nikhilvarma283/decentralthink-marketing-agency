"""Dental practice model"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.database import Base


class Practice(Base):
    __tablename__ = "practices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    practice_name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    num_dentists = Column(String, nullable=True)
    patient_base_estimate = Column(Integer, nullable=True)
    pain_point = Column(String, nullable=True)
    marketing_budget = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    status = Column(String, default="onboarding")  # onboarding, discovery, approved, active, paused, cancelled
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="practices")
    agents = relationship("Agent", back_populates="practice")

    def __repr__(self):
        return f"<Practice {self.practice_name}>"
