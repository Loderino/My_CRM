from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from CRM.database.models import Payment
from CRM.database.repositories.base import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    """Репозиторий для работы с платежами"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, Payment)
    
    async def get_by_order(self, order_id: int) -> list[Payment]:
        """Получить все платежи по заказу"""
        result = await self.session.execute(
            select(Payment)
            .where(Payment.order_id == order_id)
            .order_by(Payment.timestamp)
        )
        return result.scalars().all()

    async def get_total(self, beg_date: datetime = None) -> dict:
        """Получить сводку по платежам всех заказов"""
        query = select(
                func.sum(Payment.amount).filter(Payment.type == "payment").label("total_payment"),
                func.sum(Payment.amount).filter(Payment.type == "tip").label("total_tip"),
                func.sum(Payment.amount).filter(Payment.type == "refund").label("total_refund"),
                func.count(Payment.id).label("payment_count")
            )
        if beg_date:
            query = query.where(Payment.timestamp >= beg_date)
        result = await self.session.execute(query)
        row = result.first()
    
        return {
            "total_payment": float(row.total_payment or 0),
            "total_tip": float(row.total_tip or 0),
            "total_refund": float(row.total_refund or 0),
            "total_received": float((row.total_payment or 0) + (row.total_tip or 0) - (row.total_refund or 0)),
            "payment_count": row.payment_count or 0
        }

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
            "total_received": float((row.total_payment or 0) + (row.total_tip or 0) - (row.total_refund or 0)),
            "payment_count": row.payment_count or 0
        }