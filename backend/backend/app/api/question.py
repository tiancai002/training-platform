"""Question Bank API Routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List, Optional

from config.database import get_db
from models.question import Question, QuestionBank, UserQuestion, WrongQuestion
from models.certificate import Certificate, CertificateLevel
from models.user import User
from app.api.auth import get_current_user
from schemas.question import (
    QuestionCreate, QuestionResponse, QuestionListResponse,
    QuestionBankResponse, WrongQuestionResponse,
    PracticeRequest, PracticeResponse, DailyQuestionResponse,
    PracticeSubmitRequest, PracticeSubmitResponse
)

router = APIRouter()


# ============== Question Bank Endpoints ==============

@router.get("/banks", response_model=List[QuestionBankResponse])
def get_question_banks(
    certificate_id: Optional[int] = None,
    level: Optional[CertificateLevel] = None,
    db: Session = Depends(get_db)
):
    """Get question banks filtered by certificate and level"""
    query = db.query(QuestionBank).filter(QuestionBank.is_active == True)
    
    if certificate_id:
        query = query.filter(QuestionBank.certificate_id == certificate_id)
    
    if level:
        query = query.join(Certificate).filter(Certificate.level == level)
    
    return query.all()


@router.get("/banks/{bank_id}", response_model=QuestionBankResponse)
def get_question_bank(bank_id: int, db: Session = Depends(get_db)):
    """Get question bank details"""
    bank = db.query(QuestionBank).filter(QuestionBank.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Question bank not found")
    return bank


# ============== Question Endpoints ==============

@router.get("/questions", response_model=QuestionListResponse)
def get_questions(
    bank_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    difficulty: Optional[str] = None,
    tag: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get questions with pagination and filters"""
    query = db.query(Question).filter(
        Question.question_bank_id == bank_id,
        Question.is_active == True
    )
    
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    
    if tag:
        query = query.filter(Question.tags.contains([tag]))
    
    total = query.count()
    questions = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "items": questions,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/questions/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Get single question (without answer for practice)"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


# ============== Practice Endpoints ==============

@router.post("/practice", response_model=PracticeResponse)
def practice(
    request: PracticeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a practice session"""
    # Build question set based on request
    query = db.query(Question).filter(Question.is_active == True)
    
    if request.bank_ids:
        query = query.filter(Question.question_bank_id.in_(request.bank_ids))
    
    if request.difficulty:
        query = query.filter(Question.difficulty.in_(request.difficulty))
    
    if request.mode == "random":
        questions = query.order_by(func.random()).limit(request.count).all()
    elif request.mode == "wrong_book":
        # Get user's wrong questions
        wrong_q_ids = db.query(WrongQuestion.question_id).filter(
            WrongQuestion.user_id == current_user.id,
            WrongQuestion.is_removed == False
        ).all()
        questions = query.filter(Question.id.in_(wrong_q_ids)).limit(request.count).all()
    else:
        questions = query.limit(request.count).all()
    
    return {
        "session_id": "session_xxx",
        "questions": questions,
        "total": len(questions)
    }


@router.post("/practice/submit")
def submit_practice(
    request_data: PracticeSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit practice answer"""
    session_id = request_data.session_id
    question_id = request_data.question_id
    user_answer = request_data.user_answer
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check answer
    is_correct = (user_answer.strip() == question.answer.strip())
    
    # Record attempt
    user_question = UserQuestion(
        user_id=current_user.id,
        question_id=question_id,
        user_answer=user_answer,
        is_correct=is_correct,
        session_id=session_id
    )
    db.add(user_question)
    
    # Update wrong book
    if not is_correct:
        wrong_q = db.query(WrongQuestion).filter(
            WrongQuestion.user_id == current_user.id,
            WrongQuestion.question_id == question_id
        ).first()
        
        if wrong_q:
            wrong_q.wrong_count += 1
            wrong_q.last_wrong_at = datetime.utcnow()
        else:
            wrong_q = WrongQuestion(
                user_id=current_user.id,
                question_id=question_id,
                wrong_count=1
            )
            db.add(wrong_q)
    
    db.commit()
    
    return {
        "is_correct": is_correct,
        "correct_answer": question.answer if not is_correct else None,
        "explanation": question.explanation
    }


# ============== Wrong Book Endpoints ==============

@router.get("/wrong-book", response_model=List[WrongQuestionResponse])
def get_wrong_book(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's wrong question book"""
    wrong_questions = db.query(WrongQuestion).filter(
        WrongQuestion.user_id == current_user.id,
        WrongQuestion.is_removed == False
    ).all()
    
    return wrong_questions


@router.post("/wrong-book/{question_id}/remove")
def remove_from_wrong_book(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove question from wrong book"""
    wrong_q = db.query(WrongQuestion).filter(
        WrongQuestion.user_id == current_user.id,
        WrongQuestion.question_id == question_id
    ).first()
    
    if wrong_q:
        wrong_q.is_removed = True
        db.commit()
    
    return {"status": "success"}


# ============== Daily Question ==============

@router.get("/daily", response_model=DailyQuestionResponse)
def get_daily_question(
    certificate_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get daily question"""
    # TODO: Implement daily question logic
    query = db.query(Question).filter(Question.is_active == True)
    
    if certificate_id:
        query = query.join(QuestionBank).filter(QuestionBank.certificate_id == certificate_id)
    
    question = query.order_by(func.random()).first()
    
    return {
        "question": question,
        "date": datetime.utcnow().date()
    }


# ============== Statistics ==============

@router.get("/stats")
def get_practice_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's practice statistics"""
    total = db.query(UserQuestion).filter(
        UserQuestion.user_id == current_user.id
    ).count()
    
    correct = db.query(UserQuestion).filter(
        UserQuestion.user_id == current_user.id,
        UserQuestion.is_correct == True
    ).count()
    
    wrong_book_count = db.query(WrongQuestion).filter(
        WrongQuestion.user_id == current_user.id,
        WrongQuestion.is_removed == False
    ).count()
    
    return {
        "total_questions": total,
        "correct_count": correct,
        "wrong_count": total - correct,
        "correct_rate": correct / total if total > 0 else 0,
        "wrong_book_size": wrong_book_count
    }
