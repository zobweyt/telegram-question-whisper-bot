from sqlalchemy.ext.asyncio import create_async_engine

from src.infrastructure.settings import settings

sqlite_async_engine = create_async_engine(settings.sqlite.url)
