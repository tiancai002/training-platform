"""Chat and Communication Models"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from config.database import Base


class ChatRoom(Base):
    """Chat room for 1-on-1 or group conversations"""
    __tablename__ = "chat_rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    room_type = Column(String(20), default="private")  # private, group, system
    
    # Participants (for private chat: 2 users)
    participant_ids = Column(String(500))  # Comma-separated user IDs
    
    # Metadata
    name = Column(String(100))  # Group name
    avatar_url = Column(String(255))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_message_at = Column(DateTime)
    
    # Relationships
    messages = relationship("ChatMessage", back_populates="room")
    
    def __repr__(self):
        return f"<ChatRoom {self.id}>"


class ChatMessage(Base):
    """Chat message"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Content
    content = Column(Text, nullable=False)
    content_type = Column(String(20), default="text")  # text, image, file, system
    
    # Metadata
    file_url = Column(String(500))
    reply_to_id = Column(Integer)  # Reply to message ID
    
    # Status
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    room = relationship("ChatRoom", back_populates="messages")
    sender = relationship("User", back_populates="chat_messages")
    
    def __repr__(self):
        return f"<ChatMessage {self.id}>"
