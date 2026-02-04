from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message, Update
from sqlalchemy.ext.asyncio import AsyncSession

import logging

from bot.models.user import User

log = logging.getLogger(__name__)


class UserActivityMiddleware(BaseMiddleware):
    """Создаёт пользователя и обновляет last_seen_at на каждое сообщение."""

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        message: Message | None = None
        if isinstance(event, Update):
            message = event.message or event.edited_message
        elif isinstance(event, Message):
            message = event

        if message and message.from_user:
            session: AsyncSession | None = data.get("db_session")
            if session is not None:
                user_id = message.from_user.id
                username = message.from_user.username
                now = datetime.now(timezone.utc)

                user = await session.get(User, user_id)
                if user is None:
                    user = User(
                        id=user_id,
                        username=username,
                        first_seen_at=now,
                        last_seen_at=now,
                    )
                    session.add(user)
                else:
                    user.username = username
                    user.last_seen_at = now

                await session.commit()
                log.debug("User activity updated: %s", user_id)

        return await handler(event, data)
