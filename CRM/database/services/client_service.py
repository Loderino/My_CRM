from sqlalchemy.ext.asyncio import AsyncSession

from CRM.database.models import Client
from CRM.database.repositories.client import ClientRepository

class ClientService:
    """Сервис для работы с клиентами"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.client_repo = ClientRepository(session)

    async def get_all_clients(self, skip, limit, order_by) -> list[Client]:
        """Получить всех клиентов с пагинацией"""
        return await self.client_repo.get_all(skip, limit, order_by)
    
    async def find_clients(self, skip: int, limit: int, search: str) -> list[Client]:
        """Получить заказы по названию или описанию"""
        return await self.client_repo.get_filtered(skip, limit, search)
    
    async def search_clients(self, string_to_find: str) -> list[Client]:
        """Поиск клиентов по имени или контактам"""
        return await self.client_repo.search(string_to_find)
    
    async def get_client(self, client_id: int) -> Client | None:
        """Получить клиента по ID"""
        return await self.client_repo.get_by_id(client_id)
    
    async def get_client_orders_stats(self, client_id: int) -> dict:
        return await self.client_repo.get_order_stats(client_id)

    async def create_client(self, **kwargs) -> Client:
        """Создать нового клиента"""
        client = await self.client_repo.create(**kwargs)
        await self.session.commit()
        return client
    
    async def update_client(self, client_id: int, **kwargs) -> Client:
        """Обновить клиента"""
        client = await self.client_repo.update(client_id, **kwargs)
        await self.session.commit()
        return client