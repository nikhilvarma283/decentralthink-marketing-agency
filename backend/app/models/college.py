"""College and student recommendations model"""
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
from datetime import datetime

from app.database import Base


class College(Base):
    __tablename__ = "colleges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    city = Column(String, nullable=True)
    college_type = Column(String, nullable=True)  # large_university, small_liberal_arts, community_college, etc.
    enrollment_size = Column(String, nullable=True)
    acceptance_rate = Column(Float, nullable=True)
    avg_sat_range = Column(JSON, nullable=True)  # {low: 1200, high: 1500}
    programs = Column(JSON, default=[])  # [engineering, business, liberal_arts, etc.]
    application_url = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    recommendations = relationship("StudentRecommendation", back_populates="college")

    def __repr__(self):
        return f"<College {self.name}>"


class StudentRecommendation(Base):
    __tablename__ = "student_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    college_id = Column(UUID(as_uuid=True), ForeignKey("colleges.id"), nullable=False)
    relevance_score = Column(Float, default=0.0)
    school_type = Column(String, nullable=True)  # reach, target, safety
    created_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="recommendations")
    college = relationship("College", back_populates="recommendations")

    def __repr__(self):
        return f"<StudentRecommendation {self.student_id} -> {self.college_id}>"
