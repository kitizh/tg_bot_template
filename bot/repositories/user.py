from __future__ import annotations

from sqlalchemy import select

from bot.models.user import User
from bot.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Репозиторий пользователей."""

    model = User

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self._session.execute(stmt)
        return result.scalars().first()
