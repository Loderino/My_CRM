from typing import AsyncGenerator, Callable, Type
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from CRM.core.engine import AsyncSessionLocal
from CRM.database.repositories.base import BaseRepository


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_repository(repo_class: Type[BaseRepository]) -> Callable:
    """
    Фабрика репозиториев
    """
    async def _get_repo(db: AsyncSession = Depends(get_db)) -> BaseRepository:
        return repo_class(db)
    return _get_repo