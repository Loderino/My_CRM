from typing import List, Optional
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from CRM.database.models import StatusLog
from CRM.database.repositories.base import BaseRepository


class StatusLogRepository(BaseRepository[StatusLog]):
    """Репозиторий для работы с историей статусов заказов"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, StatusLog)
    
    async def get_by_order(self, order_id: int) -> List[StatusLog]:
        """Получить всю историю статусов по заказу"""
        result = await self.session.execute(
            select(StatusLog)
            .where(StatusLog.order_id == order_id)
            .order_by(StatusLog.timestamp)
        )
        return result.scalars().all()
    
    async def get_current_status(self, order_id: int) -> Optional[StatusLog]:
        """Получить последний статус по заказу"""
        result = await self.session.execute(
            select(StatusLog)
            .where(StatusLog.order_id == order_id)
            .order_by(desc(StatusLog.timestamp))
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    async def add_status(self, order_id: int, status: str) -> StatusLog:
        """Добавить запись о смене статуса"""
        return await self.create(
            order_id=order_id,
            status=status
        )
    
    async def get_status_history(
        self, 
        order_id: int, 
        limit: int = 10
    ) -> List[StatusLog]:
        """Получить последние N записей статусов"""
        result = await self.session.execute(
            select(StatusLog)
            .where(StatusLog.order_id == order_id)
            .order_by(desc(StatusLog.timestamp))
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_orders_by_status(
        self, 
        status: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[StatusLog]:
        """Найти заказы по последнему статусу"""
        subquery = (
            select(
                StatusLog.order_id,
                func.max(StatusLog.timestamp).label('max_ts')
            )
            .group_by(StatusLog.order_id)
            .subquery()
        )
        
        result = await self.session.execute(
            select(StatusLog)
            .join(
                subquery,
                (StatusLog.order_id == subquery.c.order_id) &
                (StatusLog.timestamp == subquery.c.max_ts)
            )
            .where(StatusLog.status == status)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()