from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select, String, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from CRM.database.models import Client
from CRM.database.repositories.base import BaseRepository


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
        """Получить клиента со всеми заказами (жадная загрузка)"""
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