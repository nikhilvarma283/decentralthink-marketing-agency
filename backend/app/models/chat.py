"""Chat message and file upload models"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

from app.database import Base


class SenderType(str, enum.Enum):
    USER = "user"
    AI = "ai"


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    session_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    sender = Column(String, nullable=False)  # user or ai
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, default=0)
    created_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="chat_messages")
    uploaded_files = relationship("UploadedFile", back_populates="message")

    def __repr__(self):
        return f"<ChatMessage {self.id}>"


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    message_id = Column(UUID(as_uuid=True), ForeignKey("chat_messages.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # mime type
    file_size = Column(Integer, nullable=False)
    extracted_text = Column(Text, nullable=True)
    storage_path = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    message = relationship("ChatMessage", back_populates="uploaded_files")

    def __repr__(self):
        return f"<UploadedFile {self.file_name}>"
