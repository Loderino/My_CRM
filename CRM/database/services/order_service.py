from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession

from CRM.database.repositories.order import OrderRepository
from CRM.database.repositories.status_log import StatusLogRepository
from CRM.database.repositories.progress_log import ProgressLogRepository
from CRM.database.repositories.payment import PaymentRepository
from CRM.database.models import Order, OrderStatus, StatusLog, ProgressLog


class OrderService:
    """Сервис для работы с заказами и связанными сущностями"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)
        self.status_log_repo = StatusLogRepository(session)
        self.progress_log_repo = ProgressLogRepository(session)
        self.payment_repo = PaymentRepository(session)
    
    async def get_order(self, order_id: int) -> Optional[Order]:
        return await self.order_repo.get_by_id(order_id)
    
    async def create_order(self, data: dict[str, Any]) -> Order:
        order = await self.order_repo.create(**data)
        await self.create_status(order.id, OrderStatus.CREATED)
        await self.session.commit()
        return order

    async def get_order_current_status(self, order_id: int) -> Optional[str]:
        return await self.status_log_repo.get_current_status(order_id)
    
    async def create_status(self, order_id: int, new_status: str) -> StatusLog:
        status = await self.status_log_repo.create(order_id=order_id, status=new_status)
        order_current_progress = await self.get_order_current_progress(order_id)
        if new_status == OrderStatus.IN_PROGRESS:
            if not order_current_progress:
                await self.progress_log_repo.create(order_id=order_id, percentage=0)
        await self.session.commit()
        return status

    async def get_order_current_progress(self, order_id: int) -> Optional[int]:
        return await self.progress_log_repo.get_current_progress(order_id)

    async def create_progress(self, order_id: int, percentage: int) -> ProgressLog:
        progress = await self.status_log_repo.create(order_id=order_id, percentage=percentage)
        await self.session.commit()
        return progress