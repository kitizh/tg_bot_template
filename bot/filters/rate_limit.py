from __future__ import annotations

from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot import rate_limits


class RateLimit(BaseFilter):
    """Фильтр rate-limit по пользователю."""

    def __init__(
        self,
        *,
        key_prefix: str = "rate",
        limit: int = 1,
        per: float = 1.0,
        notify: bool = True,
    ) -> None:
        self.key_prefix = key_prefix
        self.limit = limit
        self.per = per
        self.notify = notify

    async def __call__(self, message: Message) -> bool:
        if not message.from_user:
            return True

        if rate_limits.default_limiter is None:
            return True

        key = f"{self.key_prefix}:{message.from_user.id}"
        allowed = await rate_limits.default_limiter.allow(
            key,
            limit=self.limit,
            per=self.per,
        )
        if allowed:
            return True

        if self.notify:
            await message.answer("Слишком часто. Попробуйте позже.")
        return False
