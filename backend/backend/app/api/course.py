"""Course API"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from config.database import get_db
from models.course import Course, CourseType

router = APIRouter()


@router.get("/list")
def get_courses(
    course_type: Optional[CourseType] = None,
    certificate_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get course list"""
    query = db.query(Course).filter(Course.status == "published")
    
    if course_type:
        query = query.filter(Course.course_type == course_type)
    
    if certificate_id:
        query = query.filter(Course.certificate_id == certificate_id)
    
    total = query.count()
    courses = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {"items": courses, "total": total, "page": page}


@router.get("/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get course details"""
    course = db.query(Course).filter(Course.id == course_id).first()
    return course
