"""Chat API"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models.user import User
from app.api.auth import get_current_user

router = APIRouter()


@router.get("/rooms")
def get_chat_rooms(current_user: User = Depends(get_current_user)):
    """Get user's chat rooms"""
    pass


@router.post("/rooms/create")
def create_chat_room(target_user_id: int, current_user: User = Depends(get_current_user)):
    """Create 1-on-1 chat room"""
    pass


@router.get("/rooms/{room_id}/messages")
def get_messages(room_id: int, current_user: User = Depends(get_current_user)):
    """Get chat messages"""
    pass
