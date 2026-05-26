"""Certificate Models"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from config.database import Base


class CertificateLevel(str, enum.Enum):
    """Certificate levels for filtering"""
    BASIC = "basic"  # 基础级
    INTERMEDIATE = "intermediate"  # 进阶级
    ADVANCED = "advanced"  # 高级
    EXPERT = "expert"  # 专家级


class CertificateType(str, enum.Enum):
    """Certificate types"""
    PROFESSIONAL = "professional"  # 职业资格证书
    SKILL = "skill"  # 技能证书
    TRAINING = "training"  # 培训证书


class Certificate(Base):
    """Certificate model - users can obtain certificates"""
    __tablename__ = "certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # 证书名称
    code = Column(String(50), unique=True, nullable=False)  # 证书编码
    
    # Classification
    type = Column(SQLEnum(CertificateType), nullable=False)
    level = Column(SQLEnum(CertificateLevel), nullable=False)
    category = Column(String(50))  # 类别/职业方向
    
    # Description
    description = Column(Text)
    requirements = Column(Text)  # 获取要求
    
    # Icon
    icon_url = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user_certificates = relationship("UserCertificate", back_populates="certificate")
    question_banks = relationship("QuestionBank", back_populates="certificate")
    courses = relationship("Course", back_populates="certificate")
    
    def __repr__(self):
        return f"<Certificate {self.name} ({self.level})>"


class UserCertificate(Base):
    """User-Certificate relationship - user's obtained certificates"""
    __tablename__ = "user_certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    certificate_id = Column(Integer, ForeignKey("certificates.id"), nullable=False)
    
    # Status
    status = Column(String(20), default="pending")  # pending, obtained, expired
    obtained_at = Column(DateTime)
    expires_at = Column(DateTime)  # 证书有效期
    
    # Certificate file
    certificate_file_url = Column(String(255))  # 用户上传或系统颁发的证书文件
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="certificates")
    certificate = relationship("Certificate", back_populates="user_certificates")
    
    def __repr__(self):
        return f"<UserCertificate user={self.user_id} cert={self.certificate_id}>"
