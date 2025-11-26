from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from src.infrastructure.settings import settings
from src.infrastructure.sqlite import SQLiteDeclarativeBase


def run_migrations_offline() -> None:
    context.configure(url=settings.sqlite.url, target_metadata=SQLiteDeclarativeBase.metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    engine = create_async_engine(settings.sqlite.url)

    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync_connection: context.configure(
                connection=sync_connection,
                target_metadata=SQLiteDeclarativeBase.metadata,
                compare_type=True,
            )
        )

        await connection.run_sync(lambda _: context.run_migrations())

    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
