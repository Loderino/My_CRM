from enum import Enum
from datetime import date
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Numeric, Date, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from CRM.core.engine import Base

class OrderStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PaymentType(str, Enum):
    PAYMENT = "payment"
    TIP = "tip"
    REFUND = "refund"

class Client(Base):
    __tablename__ = "client"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    contacts = Column(JSON, default={})
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    orders = relationship("Order", back_populates="client", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    instruments = Column(JSON, nullable=False, default=list)
    contract_price = Column(Numeric(10, 2), nullable=True)
    created_date = Column(Date, nullable=False, default=date.today)
    deadline_date = Column(Date, nullable=True)
    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"), nullable=False)

    client = relationship("Client", back_populates="orders")
    progress_logs = relationship("ProgressLog", back_populates="order", cascade="all, delete-orphan")
    status_logs = relationship("StatusLog", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")
     
    def __repr__(self):
        return f"<Order(id={self.id}, title='{self.title}')>"
    
class ProgressLog(Base):
    __tablename__ = "progress_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    percentage = Column(Integer, nullable=False, default=0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    order_id = Column(Integer, ForeignKey("order.id"))

    order = relationship("Order", back_populates="progress_logs")

    def __repr__(self):
        return f"<ProgressLog(id={self.id}, percentage='{self.percentage}')>"

class StatusLog(Base):
    __tablename__ = "status_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("order.id", ondelete="CASCADE"), nullable=False)
    status = Column(SQLAlchemyEnum(OrderStatus), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    order = relationship("Order", back_populates="status_logs")

    def __repr__(self):
        return f"<StatusLog(id={self.id}, status='{self.status}')>"


class Payment(Base):
    __tablename__ = "payment"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("order.id", ondelete="CASCADE"), nullable=False)
    type = Column(SQLAlchemyEnum(PaymentType), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    order = relationship("Order", back_populates="payments")