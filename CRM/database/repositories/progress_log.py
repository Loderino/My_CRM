from typing import Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from CRM.database.models import ProgressLog
from CRM.database.repositories.base import BaseRepository


class ProgressLogRepository(BaseRepository[ProgressLog]):
    """Репозиторий для работы с историей прогресса заказов"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProgressLog)
    
    async def get_by_order(self, order_id: int) -> list[ProgressLog]:
        """Получить всю историю прогресса по заказу"""
        result = await self.session.execute(
            select(ProgressLog)
            .where(ProgressLog.order_id == order_id)
            .order_by(ProgressLog.timestamp)
        )
        return result.scalars().all()
    
    async def get_current_progress(self, order_id: int) -> Optional[ProgressLog]:
        """Получить последнюю запись прогресса по заказу"""
        result = await self.session.execute(
            select(ProgressLog)
            .where(ProgressLog.order_id == order_id)
            .order_by(desc(ProgressLog.timestamp))
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    async def add_progress(self, order_id: int, percentage: int) -> ProgressLog:
        """Добавить запись о прогрессе"""
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        
        return await self.create(
            order_id=order_id,
            percentage=percentage
        )
    
    async def get_progress_history(
        self, 
        order_id: int,
        limit: int = 10
    ) -> list[ProgressLog]:
        """Получить последние N записей прогресса"""
        result = await self.session.execute(
            select(ProgressLog)
            .where(ProgressLog.order_id == order_id)
            .order_by(desc(ProgressLog.timestamp))
            .limit(limit)
        )
        return result.scalars().all()