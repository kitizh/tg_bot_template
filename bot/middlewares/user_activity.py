from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.repositories.user import UserRepository


class UserActivityMiddleware(BaseMiddleware):
    """Создаёт пользователя и обновляет last_seen_at на каждое сообщение."""

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        message = event.message or event.edited_message

        if message and message.from_user:
            session: AsyncSession | None = data.get("db_session")
            if session is not None:
                user_id = message.from_user.id
                username = message.from_user.username
                repo = UserRepository(session)
                now = datetime.now(timezone.utc)
                user = await repo.get_or_create_user(user_id=user_id, username=username, now=now)
                await repo.last_user_activity(user, username=username, now=now)
        return await handler(event, data)
