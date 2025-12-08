import secrets

from src.sqlite import User, UserSQLiteRepository


class UserService:
    def __init__(self, *, user_sqlite_repository: UserSQLiteRepository):
        self.user_sqlite_repository = user_sqlite_repository

    async def get_or_create_user_by_id(self, id: int) -> User:
        return await self.get_user_by_id(id) or await self.create_user_by_id(id)

    async def get_user_by_id(self, id: int) -> User | None:
        return await self.user_sqlite_repository.get_by_id(id)

    async def get_user_by_url(self, url: str) -> User | None:
        return await self.user_sqlite_repository.get_by_url(url)

    async def create_user_by_id(self, id: int) -> User:
        user = User()

        user.id = id
        user.url = await self.generate_unique_user_url()

        return await self.user_sqlite_repository.create(user)

    async def update_user_url(self, user: User, *, url: str) -> None:
        user.url = url
        user.url_visit_count = 0

        await self.user_sqlite_repository.update(user)

    async def increment_user_url_visit_count_by_id(self, id: int) -> None:
        user = await self.get_user_by_id(id)

        if user is None:
            return

        user.url_visit_count = user.url_visit_count + 1

        await self.user_sqlite_repository.update(user)

    async def generate_unique_user_url(self, *, length: int = 6, max_retries: int = 5) -> str:
        for _ in range(max_retries):
            url = secrets.token_urlsafe(length - 2)[:length]
            user = await self.get_user_by_url(url)

            if user is not None:
                continue

            return url

        return await self.generate_unique_user_url(length=length + 1)
