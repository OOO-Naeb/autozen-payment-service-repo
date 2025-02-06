from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from src.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_async_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with async_session_maker() as session:
        yield session
