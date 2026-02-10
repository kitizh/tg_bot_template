from __future__ import annotations

from datetime import datetime, timezone

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

    async def get_or_create_user(
        self,
        *,
        user_id: int,
        username: str | None,
        now: datetime | None = None,
    ) -> User:
        current_time = now or datetime.now(timezone.utc)
        user: User | None = await self._session.get(User, user_id)
        if user is None:
            user = User(
                id=user_id,
                username=username,
                first_seen_at=current_time,
                last_seen_at=current_time,
            )
            self._session.add(user)
            await self._session.flush()
            return user

        user.username = username
        return user

    async def last_user_activity(
        self,
        user: User,
        *,
        username: str | None,
        now: datetime | None = None,
    ) -> None:
        current_time = now or datetime.now(timezone.utc)
        user.username = username
        user.last_seen_at = current_time
        await self._session.flush()
