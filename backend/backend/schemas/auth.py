"""Auth Schemas"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    """Token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data"""
    username: Optional[str] = None


class UserBase(BaseModel):
    """User base schema"""
    username: str
    email: EmailStr
    nickname: Optional[str] = None


class UserCreate(UserBase):
    """User create schema"""
    password: str


class UserLogin(BaseModel):
    """User login schema"""
    username: str
    password: str


class UserResponse(UserBase):
    """User response schema"""
    id: int
    role: str
    is_active: bool
    created_at: datetime
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    is_verified: Optional[bool] = None
    learning_stats: Optional[dict] = None
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """User update schema"""
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
