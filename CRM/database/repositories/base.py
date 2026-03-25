from typing import Generic, TypeVar, Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from CRM.core.engine import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Базовый репозиторий с общими CRUD операциями"""
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Получить запись по ID"""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = "id"
    ) -> list[ModelType]:
        """Получить все записи с пагинацией"""
        query = select(self.model).offset(skip).limit(limit)
        if order_by:
            query = query.order_by(order_by)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def create(self, **kwargs) -> ModelType:
        """Создать новую запись"""
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj
    
    async def update(
        self, 
        _id: int, 
        **kwargs
    ) -> Optional[ModelType]:
        """Обновить запись"""
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        
        if not update_data:
            return await self.get_by_id(_id)
        
        await self.session.execute(
            update(self.model)
            .where(self.model.id == _id)
            .values(**update_data)
        )
        await self.session.commit()
        return await self.get_by_id(id)
    
    async def delete(self, id: int) -> bool:
        """Удалить запись"""
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.commit()
        return result.rowcount > 0
    
    async def count(self) -> int:
        """Количество записей"""
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar()