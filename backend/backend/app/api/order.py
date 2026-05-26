"""Order API"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models.user import User
from app.api.auth import get_current_user

router = APIRouter()


@router.post("/create")
def create_order(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create order"""
    pass


@router.get("/list")
def get_order_list(current_user: User = Depends(get_current_user)):
    """Get user's order list"""
    pass


@router.get("/{order_id}")
def get_order(order_id: int):
    """Get order details"""
    pass
