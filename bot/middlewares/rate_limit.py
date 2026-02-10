from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message, Update

from bot.core.config import settings
from bot import rate_limits


class RateLimitMiddleware(BaseMiddleware):
    """Глобальный rate-limit для сообщений."""

    @staticmethod
    def _is_exempt_command(message: Message) -> bool:
        if not message.text:
            return False
        command = message.text.split(maxsplit=1)[0]
        return command in {"/broadcast"}

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

        if not message or not message.from_user:
            return await handler(event, data)

        if message.from_user.id in settings.admin_ids:
            return await handler(event, data)

        if rate_limits.default_limiter is None:
            return await handler(event, data)

        if self._is_exempt_command(message):
            return await handler(event, data)

        user_id = message.from_user.id
        if message.text and message.text.startswith("/"):
            key = f"rate:cmd:{user_id}"
            limit = settings.command_rate_limit_limit
            period = settings.command_rate_limit_period
        else:
            key = f"rate:msg:{user_id}"
            limit = settings.rate_limit_limit
            period = settings.rate_limit_period

        allowed = await rate_limits.default_limiter.allow(key, limit=limit, per=period)
        if allowed:
            return await handler(event, data)

        if settings.rate_limit_notify:
            await message.answer("Слишком часто. Попробуйте позже.")
        return None
