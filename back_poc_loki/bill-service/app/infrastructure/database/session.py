from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (  # type: ignore
    create_async_engine,
    AsyncSession,
)

from ..config.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    connect_args={
        "server_settings": {
            "search_path": settings.DB_SCHEMA
        },
        "timeout": settings.DB_CONNECT_TIMEOUT,
        "command_timeout": settings.DB_COMMAND_TIMEOUT,
    },
    pool_size=settings.DB_POOL_SIZE,
)


SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
