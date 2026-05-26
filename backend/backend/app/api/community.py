"""Community API"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from config.database import get_db
from models.community import CommunityPost, CommunityComment, CommunityLike, CommunityCategory
from models.user import User
from app.api.auth import get_current_user

router = APIRouter()


@router.get("/posts")
def get_posts(
    category_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get community posts"""
    query = db.query(CommunityPost).filter(CommunityPost.is_deleted == False)
    
    if category_id:
        query = query.filter(CommunityPost.category_id == category_id)
    
    query = query.order_by(CommunityPost.is_pinned.desc(), CommunityPost.created_at.desc())
    
    total = query.count()
    posts = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # Include author information
    items = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
            "author": None,
            "category_id": post.category_id,
            "tags": post.tags,
            "view_count": post.view_count,
            "like_count": post.like_count,
            "comment_count": post.comment_count,
            "is_pinned": post.is_pinned,
            "is_locked": post.is_locked,
            "is_deleted": post.is_deleted,
            "created_at": post.created_at.isoformat() if post.created_at else None,
            "updated_at": post.updated_at.isoformat() if post.updated_at else None
        }
        
        # Get author info
        author = db.query(User).filter(User.id == post.author_id).first()
        if author:
            post_dict["author"] = {
                "id": author.id,
                "nickname": author.nickname,
                "avatar_url": author.avatar_url,
                "role": author.role
            }
        
        items.append(post_dict)
    
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.post("/posts/create")
def create_post(
    title: str,
    content: str,
    category_id: Optional[int] = None,
    tags: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create community post"""
    post = CommunityPost(
        title=title,
        content=content,
        author_id=current_user.id,
        category_id=category_id,
        tags=tags
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get post details"""
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post or post.is_deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Increment view count
    post.view_count += 1
    db.commit()
    
    return post


@router.post("/posts/{post_id}/like")
def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Like a post"""
    # Check if already liked
    existing = db.query(CommunityLike).filter(
        CommunityLike.post_id == post_id,
        CommunityLike.user_id == current_user.id
    ).first()
    
    if existing:
        # Unlike
        db.delete(existing)
        post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
        post.like_count -= 1
    else:
        # Like
        like = CommunityLike(post_id=post_id, user_id=current_user.id)
        db.add(like)
        post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
        post.like_count += 1
    
    db.commit()
    return {"status": "success", "like_count": post.like_count}


@router.post("/posts/{post_id}/comment")
def add_comment(
    post_id: int,
    content: str,
    parent_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add comment to post"""
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment = CommunityComment(
        post_id=post_id,
        author_id=current_user.id,
        content=content,
        parent_id=parent_id
    )
    db.add(comment)
    
    # Increment comment count
    post.comment_count += 1
    
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get community categories"""
    categories = db.query(CommunityCategory).filter(
        CommunityCategory.is_active == True
    ).order_by(CommunityCategory.sort_order).all()
    return categories
