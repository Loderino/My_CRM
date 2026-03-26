from typing import Optional, Any
from datetime import timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession

from CRM.database.repositories.order import OrderRepository
from CRM.database.repositories.payment import PaymentRepository
from CRM.database.models import Order, OrderStatus, Payment, PaymentType, ProgressLog, StatusLog


class PaymentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)
        self.payment_repo = PaymentRepository(session)

    async def get_total_earned(self, period: timedelta = None) -> dict:
        if period:
            return await self.payment_repo.get_total(datetime.now() - period)
        return await self.payment_repo.get_total()