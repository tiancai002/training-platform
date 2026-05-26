"""Community Forum Models"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from config.database import Base


class CommunityPost(Base):
    """Community post (like Tieba posts)"""
    __tablename__ = "community_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    
    # Author
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Category
    category_id = Column(Integer, ForeignKey("community_categories.id"))
    tags = Column(String(500))  # Comma-separated tags
    
    # Statistics
    view_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    
    # Status
    is_pinned = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = relationship("User", back_populates="posts")
    category = relationship("CommunityCategory", back_populates="posts")
    comments = relationship("CommunityComment", back_populates="post")
    likes = relationship("CommunityLike", back_populates="post")
    
    def __repr__(self):
        return f"<CommunityPost {self.title}>"


class CommunityComment(Base):
    """Community comment"""
    __tablename__ = "community_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Content
    content = Column(Text, nullable=False)
    parent_id = Column(Integer)  # For nested replies
    
    # Status
    is_deleted = Column(Boolean, default=False)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("CommunityPost", back_populates="comments")
    
    def __repr__(self):
        return f"<CommunityComment {self.id}>"


class CommunityLike(Base):
    """Post like"""
    __tablename__ = "community_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("CommunityPost", back_populates="likes")
    
    def __repr__(self):
        return f"<CommunityLike post={self.post_id} user={self.user_id}>"


class CommunityCategory(Base):
    """Community category"""
    __tablename__ = "community_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    icon = Column(String(50))
    
    # Order
    sort_order = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = relationship("CommunityPost", back_populates="category")
    
    def __repr__(self):
        return f"<CommunityCategory {self.name}>"
