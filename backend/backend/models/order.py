"""Order and Payment Models"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from config.database import Base


class OrderStatus(str, enum.Enum):
    """Order status"""
    PENDING = "pending"  # 待支付
    PAID = "paid"  # 已支付
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消
    REFUNDED = "refunded"  # 已退款


class OrderType(str, enum.Enum):
    """Order type"""
    COURSE = "course"  # 课程
    QUESTION_BANK = "question_bank"  # 题库
    ONE_ON_ONE = "one_on_one"  # 一对一辅导
    MEMBERSHIP = "membership"  # 会员


class Order(Base):
    """Order model"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Type
    order_type = Column(SQLEnum(OrderType), nullable=False)
    
    # Items
    items = Column(JSON, nullable=False)  # 订单 items [{type, id, name, price, quantity}]
    
    # Amount
    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0)
    final_amount = Column(Float, nullable=False)
    
    # Status
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)
    
    # Payment
    payment_method = Column(String(20))  # wechat, alipay, stripe
    payment_time = Column(DateTime)
    transaction_id = Column(String(100))  # 第三方支付交易 ID
    
    # Metadata
    remark = Column(String(500))
    extra_data = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = Column(DateTime)
    
    # Relationships
    payments = relationship("Payment", back_populates="order")
    
    def __repr__(self):
        return f"<Order {self.order_no}>"


class Payment(Base):
    """Payment records"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    
    # Payment info
    payment_no = Column(String(50), unique=True)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(20), nullable=False)
    
    # Third-party info
    transaction_id = Column(String(100))
    channel = Column(String(20))  # wechat, alipay, stripe
    
    # Status
    status = Column(String(20), default="pending")  # pending, success, failed
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime)
    
    # Relationships
    order = relationship("Order", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment {self.payment_no}>"
