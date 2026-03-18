from datetime import date
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from CRM.core.engine import Base

class Client(Base):
    __tablename__ = "client"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    contacts = Column(JSON, default={})
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
     
    def __repr__(self):
        return f"<Order(id={self.id}, title='{self.title}')>"