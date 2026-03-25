from typing import List, Optional
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from CRM.database.models import Payment
from CRM.database.repositories.base import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    """Репозиторий для работы с платежами"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, Payment)
    
    async def get_by_order(self, order_id: int) -> List[Payment]:
        """Получить все платежи по заказу"""
        result = await self.session.execute(
            select(Payment)
            .where(Payment.order_id == order_id)
            .order_by(Payment.timestamp)
        )
        return result.scalars().all()
    
    async def get_received_amount(self, order_id: int) -> float:
        """Получить сумму всех полученных платежей (payment + tip)"""
        result = await self.session.execute(
            select(func.sum(Payment.amount))
            .where(Payment.order_id == order_id)
            .where(Payment.type.in_(["payment", "tip"]))
        )
        return float(result.scalar() or 0)
    
    async def get_payments_by_type(
        self, 
        order_id: int, 
        payment_type: str
    ) -> List[Payment]:
        """Получить платежи определённого типа по заказу"""
        result = await self.session.execute(
            select(Payment)
            .where(Payment.order_id == order_id)
            .where(Payment.type == payment_type)
            .order_by(Payment.timestamp)
        )
        return result.scalars().all()
    
    async def get_total_by_order(self, order_id: int) -> dict:
        """Получить сводку по платежам заказа"""
        result = await self.session.execute(
            select(
                func.sum(Payment.amount).filter(Payment.type == "payment").label("total_payment"),
                func.sum(Payment.amount).filter(Payment.type == "tip").label("total_tip"),
                func.sum(Payment.amount).filter(Payment.type == "refund").label("total_refund"),
                func.count(Payment.id).label("payment_count")
            )
            .where(Payment.order_id == order_id)
        )
        row = result.first()
        
        return {
            "total_payment": float(row.total_payment or 0),
            "total_tip": float(row.total_tip or 0),
            "total_refund": float(row.total_refund or 0),
            "total_received": float((row.total_payment or 0) + (row.total_tip or 0)),
            "payment_count": row.payment_count or 0
        }
    
    async def get_last_payment(self, order_id: int) -> Optional[Payment]:
        """Получить последний платёж по заказу"""
        result = await self.session.execute(
            select(Payment)
            .where(Payment.order_id == order_id)
            .order_by(desc(Payment.timestamp))
            .limit(1)
        )
        return result.scalar_one_or_none()