from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession

from CRM.database.repositories.order import OrderRepository
from CRM.database.repositories.status_log import StatusLogRepository
from CRM.database.repositories.progress_log import ProgressLogRepository
from CRM.database.repositories.payment import PaymentRepository
from CRM.database.models import Order, OrderStatus, Payment, ProgressLog, StatusLog


class OrderService:
    """Сервис для работы с заказами и связанными сущностями"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)
        self.status_log_repo = StatusLogRepository(session)
        self.progress_log_repo = ProgressLogRepository(session)
        self.payment_repo = PaymentRepository(session)
    
    # ========== ORDERS ==========

    async def get_all_orders(self, skip, limit, order_by) -> list[Order]:
        """Получить все заказы с пагинацией"""
        return await self.order_repo.get_all(skip, limit, order_by)

    async def get_order(self, order_id: int) -> Optional[Order]:
        """Получить детальную информацию о заказе по id"""
        return await self.order_repo.get_by_id(order_id)
    
    async def get_active_orders(self):
        """Получить заказы, у которых статус не 'завершён'"""
        return await self.order_repo.get_active_orders()
    
    async def create_order(self, data: dict[str, Any]) -> Order:
        """Добавить запись о заказе"""
        order = await self.order_repo.create(**data)
        await self.create_status(order.id, OrderStatus.CREATED)
        await self.session.commit()
        return order
    
    # ========== STATUSES ==========

    async def get_order_statuses_history(self, order_id: int) -> list[StatusLog]:
        """Получить историю изменений статусов заказа"""
        return await self.status_log_repo.get_by_order(order_id)

    async def get_order_current_status(self, order_id: int) -> Optional[str]:
        """Получить текущий статус заказа"""
        return await self.status_log_repo.get_current_status(order_id)
    
    async def create_status(self, order_id: int, new_status: str) -> StatusLog:
        """Добавить запись о статусе заказа"""
        status = await self.status_log_repo.create(order_id=order_id, status=new_status)
        order_current_progress = await self.get_order_current_progress(order_id)
        if new_status == OrderStatus.IN_PROGRESS:
            if not order_current_progress:
                await self.progress_log_repo.create(order_id=order_id, percentage=0)
        await self.session.commit()
        return status

    # ========== PROGRESS ==========

    async def get_order_progress_history(self, order_id: int) -> list[ProgressLog]:
        """Получить историю изменения прогресса выполнения заказа"""
        return await self.progress_log_repo.get_by_order(order_id)

    async def get_order_current_progress(self, order_id: int) -> Optional[int]:
        """Получить текущий прогресс выполнения заказа"""
        return await self.progress_log_repo.get_current_progress(order_id)

    async def create_progress(self, order_id: int, percentage: int) -> ProgressLog:
        """Создать запись о прогрессе выполнения заказа"""
        progress = await self.status_log_repo.create(order_id=order_id, percentage=percentage)
        await self.session.commit()
        return progress
    
    # ========== PAYMENTS ==========

    async def get_order_payments(self, order_id: int) -> list[Payment]:
        """Получить все платежи по заказу"""
        return await self.payment_repo.get_by_order(order_id)
    
    async def create_payment(self, order_id: int, type: str, amount: float) -> Payment:
        """Добавить запись о платеже"""
        payment = await self.payment_repo.create(order_id=order_id, type=type, amount=amount)
        await self.session.commit()
        return payment