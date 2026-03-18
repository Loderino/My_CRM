from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from CRM.core.config import settings


sync_engine = create_engine(settings.database_url)
async_engine = create_async_engine(settings.database_url.replace("postgresql://", "postgresql+asyncpg://"))

# Фабрика сессий
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession)
Base = declarative_base()