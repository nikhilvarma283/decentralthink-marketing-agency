"""High school student model"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
from datetime import datetime

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    grade = Column(Integer, nullable=False)  # 9-12
    high_school_name = Column(String, nullable=True)
    primary_interest = Column(String, nullable=True)
    additional_interests = Column(JSON, default=[])
    goal_text = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    subscription_status = Column(String, default="free")  # free, premium, cancelled
    subscription_tier = Column(String, nullable=True)  # monthly or yearly
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="students")
    recommendations = relationship("StudentRecommendation", back_populates="student")

    def __repr__(self):
        return f"<Student {self.user_id}>"
