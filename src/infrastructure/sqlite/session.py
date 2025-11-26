from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.infrastructure.sqlite.engine import sqlite_async_engine

SQLiteAsyncSession = async_sessionmaker(
    bind=sqlite_async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
