import base64
import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.user import User


class UserService:
    def __init__(self, *, sqlite_session: AsyncSession):
        self.sqlite_session = sqlite_session

    async def get_or_create_user_by_id(self, id: int) -> User:
        return await self.get_user_by_id(id) or await self.create_user_by_id(id)

    async def get_user_by_id(self, id: int) -> User | None:
        statement = select(User).where(User.id == id)
        result = await self.sqlite_session.execute(statement)

        return result.scalar_one_or_none()

    async def get_user_by_url(self, url: str) -> User | None:
        statement = select(User).where(User.url == url)
        result = await self.sqlite_session.execute(statement)

        return result.scalar_one_or_none()

    async def create_user_by_id(self, id: int) -> User:
        user = User()

        user.id = id
        user.url = await self.generate_unique_user_url()

        self.sqlite_session.add(user)

        await self.sqlite_session.commit()
        await self.sqlite_session.refresh(user)

        return user

    async def update_user_url(self, user: User, *, url: str) -> None:
        user.url = url
        user.url_visit_count = 0

        await self.sqlite_session.commit()
        await self.sqlite_session.refresh(user)

    async def increment_user_url_visit_count_by_id(self, id: int) -> None:
        existing_user = await self.get_user_by_id(id)

        if existing_user is None:
            return

        existing_user.url_visit_count = existing_user.url_visit_count + 1

        await self.sqlite_session.commit()
        await self.sqlite_session.refresh(existing_user)

    async def generate_unique_user_url(self) -> str:
        while True:
            url = self.generate_user_url()
            existing_user = await self.get_user_by_url(url)
            if existing_user is None:
                return url

    def generate_user_url(self) -> str:
        lengths = [6, 6, 6, 8, 8, 8, 10, 10, 12, 16]
        length = secrets.choice(lengths)
        random_bytes = secrets.token_bytes(48)
        url = base64.urlsafe_b64encode(random_bytes).decode("ascii").rstrip("=")
        return url[:length]
