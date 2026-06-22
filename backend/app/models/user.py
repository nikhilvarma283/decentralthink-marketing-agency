"""User model"""
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

from app.database import Base


class UserRole(str, enum.Enum):
    DENTIST = "dentist"
    HIGH_SCHOOLER = "high_schooler"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    stripe_customer_id = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chat_messages = relationship("ChatMessage", back_populates="user")
    practices = relationship("Practice", back_populates="user")
    students = relationship("Student", back_populates="user")
    plans = relationship("Plan", back_populates="user")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User {self.email}>"
