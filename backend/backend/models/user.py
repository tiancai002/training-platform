"""User Models"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from config.database import Base


class UserRole(str, enum.Enum):
    """User roles - single admin backend, no hierarchy"""
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"
    GUEST = "guest"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    nickname = Column(String(50))
    avatar_url = Column(String(255))
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)
    
    # Learning data (cached)
    learning_stats = Column(JSON, default=dict)  # {total_questions, correct_rate, study_days, etc.}
    
    # Relationships
    certificates = relationship("UserCertificate", back_populates="user", cascade="all, delete-orphan")
    wrong_questions = relationship("WrongQuestion", back_populates="user", cascade="all, delete-orphan")
    course_orders = relationship("CourseOrder", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="sender", cascade="all, delete-orphan")
    posts = relationship("CommunityPost", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.username}>"
