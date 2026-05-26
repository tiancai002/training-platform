"""Question Schemas"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any
from datetime import datetime


# ============== Question Bank Schemas ==============

class QuestionBankBase(BaseModel):
    """Question bank base schema"""
    name: str
    description: Optional[str] = None
    certificate_id: int


class QuestionBankCreate(QuestionBankBase):
    """Question bank create schema"""
    pass


class QuestionBankResponse(QuestionBankBase):
    """Question bank response schema"""
    id: int
    code: Optional[str] = None
    total_questions: int = 0
    is_active: bool = True
    
    class Config:
        from_attributes = True


# ============== Question Schemas ==============

class QuestionBase(BaseModel):
    """Question base schema"""
    content: str
    content_type: str = "text"
    options: Optional[List[dict]] = None
    answer: str
    answer_type: str = "single"
    difficulty: str = "medium"
    tags: Optional[List[str]] = None
    explanation: Optional[str] = None


class QuestionCreate(QuestionBase):
    """Question create schema"""
    question_bank_id: int


class QuestionUpdate(BaseModel):
    """Question update schema"""
    content: Optional[str] = None
    options: Optional[List[dict]] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class QuestionResponse(QuestionBase):
    """Question response schema"""
    id: int
    question_bank_id: int
    total_attempts: int = 0
    correct_rate: float = 0.0
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuestionListResponse(BaseModel):
    """Question list response"""
    items: List[QuestionResponse]
    total: int
    page: int
    page_size: int


# ============== Practice Schemas ==============

class PracticeRequest(BaseModel):
    """Practice request schema"""
    bank_ids: Optional[List[int]] = None
    count: int = Field(10, ge=1, le=100)
    mode: str = "random"  # random, sequential, wrong_book
    difficulty: Optional[List[str]] = None


class PracticeResponse(BaseModel):
    """Practice response schema"""
    session_id: str
    questions: List[QuestionResponse]
    total: int


class PracticeSubmitRequest(BaseModel):
    """Practice submit request"""
    session_id: str
    question_id: int
    user_answer: str


class PracticeSubmitResponse(BaseModel):
    """Practice submit response"""
    is_correct: bool
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None


# ============== Wrong Book Schemas ==============

class WrongQuestionResponse(BaseModel):
    """Wrong question response"""
    id: int
    question_id: int
    question_content: str
    wrong_count: int
    correct_count: int
    remove_threshold: int
    last_wrong_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============== Daily Question Schemas ==============

class DailyQuestionResponse(BaseModel):
    """Daily question response"""
    question: QuestionResponse
    date: str
    
    @field_validator('date', mode='before')
    @classmethod
    def date_to_str(cls, v):
        if isinstance(v, str):
            return v
        return str(v) if v else None


# ============== Statistics Schemas ==============

class PracticeStats(BaseModel):
    """Practice statistics"""
    total_questions: int
    correct_count: int
    wrong_count: int
    correct_rate: float
    wrong_book_size: int
