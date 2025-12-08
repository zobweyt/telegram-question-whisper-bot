from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.sqlite import User


class UserSQLiteRepository:
    def __init__(self, *, sqlite_session: AsyncSession):
        self.sqlite_session = sqlite_session

    async def get_by_id(self, id: int) -> User | None:
        statement = select(User).where(User.id == id)
        result = await self.sqlite_session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_url(self, url: str) -> User | None:
        statement = select(User).where(User.url == url)
        result = await self.sqlite_session.execute(statement)

        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.sqlite_session.add(user)

        await self.sqlite_session.commit()
        await self.sqlite_session.refresh(user)

        return user

    async def update(self, user: User) -> User:
        await self.sqlite_session.commit()
        await self.sqlite_session.refresh(user)

        return user
