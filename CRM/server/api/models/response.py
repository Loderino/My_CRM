from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class StatusLogResponse(BaseModel):
    id: int
    status: str
    timestamp: datetime

class ProgressLogResponse(BaseModel):
    id: int
    percentage: int
    timestamp: datetime

class PaymentResponse(BaseModel):
    id: int
    type: str
    amount: float
    timestamp: datetime

class OrderResponse(BaseModel):
    id: int
    client_id: int
    title: str
    description: Optional[str]
    instruments: list[str]
    contract_price: float
    deadline_date: Optional[datetime]
    created_date: datetime

class DetailedOrderResponse(OrderResponse):
    id: int
    client_id: int
    title: str
    description: Optional[str]
    instruments: list[str]
    contract_price: float
    deadline_date: Optional[datetime]
    created_date: datetime
    status_logs: list[StatusLogResponse]
    progress_logs: list[ProgressLogResponse]
    payments: list[PaymentResponse]