"""Course Models"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from config.database import Base


class CourseType(str, enum.Enum):
    """Course types"""
    LIVE = "live"  # 直播课程
    RECORDED = "recorded"  # 录播课程
    OFFLINE = "offline"  # 线下课程
    ONE_ON_ONE = "one_on_one"  # 一对一辅导


class CourseStatus(str, enum.Enum):
    """Course status"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ENDED = "ended"
    CANCELLED = "cancelled"


class Course(Base):
    """Course model"""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(500))
    
    # Type
    course_type = Column(SQLEnum(CourseType), nullable=False)
    status = Column(SQLEnum(CourseStatus), default=CourseStatus.DRAFT)
    
    # Association
    certificate_id = Column(Integer, ForeignKey("certificates.id"))
    instructor_id = Column(Integer, ForeignKey("users.id"))
    
    # Content
    description = Column(Text)
    cover_url = Column(String(255))
    video_url = Column(String(500))  # 录播视频 URL
    live_url = Column(String(500))  # 直播链接 (第三方平台)
    
    # Schedule (for live/offline)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String(200))  # 线下地点或直播房间号
    
    # Price
    price = Column(Float, default=0.0)
    original_price = Column(Float)
    
    # Capacity
    max_students = Column(Integer)
    enrolled_count = Column(Integer, default=0)
    
    # Metadata
    duration = Column(Integer)  # 时长 (分钟)
    tags = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    certificate = relationship("Certificate", back_populates="courses")
    orders = relationship("CourseOrder", back_populates="course", cascade="all, delete-orphan")
    progress_records = relationship("CourseProgress", back_populates="course", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Course {self.title}>"


class CourseOrder(Base):
    """Course order - user's course purchases"""
    __tablename__ = "course_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    # Payment
    price = Column(Float, nullable=False)
    payment_status = Column(String(20), default="pending")  # pending, paid, refunded
    payment_time = Column(DateTime)
    
    # Status
    status = Column(String(20), default="active")  # active, completed, cancelled
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="course_orders")
    course = relationship("Course", back_populates="orders")
    
    def __repr__(self):
        return f"<CourseOrder {self.order_no}>"


class CourseProgress(Base):
    """Course learning progress"""
    __tablename__ = "course_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    # Progress
    progress = Column(Float, default=0.0)  # 学习进度 0-100%
    last_position = Column(Integer, default=0)  # 视频最后位置 (秒)
    
    # Status
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="progress_records")
    
    def __repr__(self):
        return f"<CourseProgress user={self.user_id} course={self.course_id}>"
