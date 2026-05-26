"""Question Bank Models"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from config.database import Base


class QuestionBank(Base):
    """Question bank - organized by certificate and level"""
    __tablename__ = "question_banks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # 题库名称
    code = Column(String(50), unique=True)  # 题库编码
    
    # Association
    certificate_id = Column(Integer, ForeignKey("certificates.id"), nullable=False)
    
    # Metadata
    description = Column(Text)
    total_questions = Column(Integer, default=0)
    
    # Settings
    is_public = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    certificate = relationship("Certificate", back_populates="question_banks")
    questions = relationship("Question", back_populates="question_bank")
    
    def __repr__(self):
        return f"<QuestionBank {self.name}>"


class Question(Base):
    """Question model"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_bank_id = Column(Integer, ForeignKey("question_banks.id"), nullable=False)
    
    # Content
    content = Column(Text, nullable=False)  # 题目内容
    content_type = Column(String(20), default="text")  # text, image, rich_text
    
    # Options (for multiple choice)
    options = Column(JSON)  # [{"key": "A", "value": "选项内容"}, ...]
    
    # Answer
    answer = Column(String(500), nullable=False)  # 正确答案
    answer_type = Column(String(20))  # single, multiple, true_false, fill_in, essay
    
    # Metadata
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    tags = Column(JSON)  # 标签列表
    explanation = Column(Text)  # 答案解析
    
    # Statistics
    total_attempts = Column(Integer, default=0)
    correct_rate = Column(Float, default=0.0)  # 正确率
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    question_bank = relationship("QuestionBank", back_populates="questions")
    user_questions = relationship("UserQuestion", back_populates="question")
    
    def __repr__(self):
        return f"<Question {self.id}>"


class UserQuestion(Base):
    """User question attempt records"""
    __tablename__ = "user_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    
    # Attempt info
    user_answer = Column(String(500))  # 用户答案
    is_correct = Column(Boolean)
    
    # Context
    session_id = Column(String(50))  # 练习会话 ID
    practice_mode = Column(String(20))  # daily, practice, exam, random
    
    # Time
    time_spent = Column(Integer)  # 耗时 (秒)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    question = relationship("Question", back_populates="user_questions")
    
    def __repr__(self):
        return f"<UserQuestion user={self.user_id} question={self.question_id}>"


class WrongQuestion(Base):
    """Wrong question book - tracks user's wrong answers"""
    __tablename__ = "wrong_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    
    # Wrong count
    wrong_count = Column(Integer, default=1)  # 答错次数
    correct_count = Column(Integer, default=0)  # 后续答对次数
    
    # Settings
    remove_threshold = Column(Integer, default=3)  # 答对几次后移除 (1/2/3/0=不移除)
    is_removed = Column(Boolean, default=False)  # 是否已移除
    
    # Last activity
    last_wrong_at = Column(DateTime)
    last_correct_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="wrong_questions")
    question = relationship("Question")
    
    def __repr__(self):
        return f"<WrongQuestion user={self.user_id} question={self.question_id}>"
