from typing import Optional
from datetime import date, timedelta
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from CRM.database.models import Order, OrderStatus, StatusLog
from CRM.database.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """Репозиторий для работы с заказами"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, Order)
    
    async def get_by_id(self, id: int, detail: bool = True) -> Optional[Order]:
        query = select(Order).where(Order.id == id)
        if detail:
            query = query.options(
                selectinload(Order.client),
                selectinload(Order.status_logs),
                selectinload(Order.progress_logs),
                selectinload(Order.payments)
            )
            
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_client(self, client_id: int) -> list[Order]:
        """Все заказы клиента"""
        result = await self.session.execute(
            select(Order)
            .where(Order.client_id == client_id)
            .order_by(Order.created_date.desc())
        )
        return result.scalars().all()


    async def get_active_orders(self) -> list[Order]:
        """Получить заказы, у которых последний статус не 'completed'"""
        subquery = (
            select(
                StatusLog.order_id,
                StatusLog.status,
                StatusLog.timestamp
            )
            .distinct(StatusLog.order_id)
            .order_by(StatusLog.order_id, desc(StatusLog.timestamp))
            .subquery()
        )
        
        result = await self.session.execute(
            select(Order)
            .join(subquery, Order.id == subquery.c.order_id)
            .where(subquery.c.status != OrderStatus.COMPLETED)
            .options(selectinload(Order.status_logs))
        )
        return result.scalars().all()
    
    async def get_upcoming_deadlines(self, days: int = 7) -> list[Order]:
        """Заказы с ближайшими дедлайнами"""
        today = date.today()
        deadline_limit = today + timedelta(days=days)
        
        result = await self.session.execute(
            select(Order)
            .where(
                and_(
                    Order.deadline_date.isnot(None),
                    Order.deadline_date <= deadline_limit,
                    Order.deadline_date >= today
                )
            )
            .order_by(Order.deadline_date)
        )
        return result.scalars().all()
    
    async def get_filtered(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> list[Order]:
        """
        Получить отфильтрованный список клиентов с пагинацией
        Возвращает (список, общее_количество)
        """
        query = select(Order)
    
        if search:
            search_filter = or_(
                Order.title.ilike(f"%{search}%"),
                Order.description.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        # Потом данные с пагинацией
        result = await self.session.execute(
            query.offset(skip).limit(limit)
        )
        clients = result.scalars().all()
        
        return clients