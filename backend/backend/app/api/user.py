"""User API"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models.user import User
from app.api.auth import get_current_user

router = APIRouter()


@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    """Get user profile"""
    return current_user


@router.get("/stats")
def get_learning_stats(current_user: User = Depends(get_current_user)):
    """Get user learning statistics"""
    return current_user.learning_stats or {}
