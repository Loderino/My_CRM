from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select, or_, String, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from CRM.database.models import Client
from CRM.database.repositories.base import BaseRepository
from CRM.database.models import Order

class ClientRepository(BaseRepository[Client]):
    """Репозиторий для работы с клиентами"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, Client)
    
    async def search_by_contact(self, contact_value: str) -> list[Client]:
        """Поиск клиента по контактам (телефон, email в JSON)"""
        result = await self.session.execute(
            select(Client).where(
                Client.contacts.cast(String).ilike(f"%{contact_value}%")
            )
        )
        return result.scalars().all()
    
    async def get_with_orders(self, client_id: int) -> Optional[Client]:
        """Получить клиента со всеми заказами"""
        result = await self.session.execute(
            select(Client)
            .where(Client.id == client_id)
            .options(selectinload(Client.orders))
        )
        return result.scalar_one_or_none()
    
    async def get_recent_clients(self, days: int = 30) -> list[Client]:
        """Клиенты, добавленные за последние N дней"""
        cutoff_date = datetime.now() - timedelta(days=days)
        result = await self.session.execute(
            select(Client)
            .where(Client.created_at >= cutoff_date)
            .order_by(Client.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_filtered(
        self,
        skip: int = 0,
        limit: int = 100,
        has_orders: Optional[bool] = None,
        search: Optional[str] = None
    ) -> tuple[list[Client], int]:
        """
        Получить отфильтрованный список клиентов с пагинацией
        Возвращает (список, общее_количество)
        """
        query = select(Client)
    
        if search:
            search_filter = or_(
                Client.name.ilike(f"%{search}%"),
                Client.contacts.cast(String).ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        if has_orders is not None:
            if has_orders:
                query = query.where(Client.orders.any())
            else:
                query = query.where(~Client.orders.any())
        
        # Сначала получаем общее количество
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.execute(count_query)
        total = total.scalar()
        
        # Потом данные с пагинацией
        result = await self.session.execute(
            query.offset(skip).limit(limit)
        )
        clients = result.scalars().all()
        
        return clients, total

    async def get_order_stats(self, client_id: int) -> dict:
        """Получить статистику по заказам клиента"""
        result = await self.session.execute(
            select(
                func.count(Order.id).label('count'),
                func.sum(Order.contract_price).label('sum')
            ).where(Order.client_id == client_id)
        )
        row = result.first()
        
        return {
            "orders_count": row.count or 0,
            "orders_sum": float(row.sum or 0)
        }