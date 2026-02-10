from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.types import MiddlewareData

class DbSessionMiddleware(BaseMiddleware):
    """Открывает DB-сессию на update и закрывает после обработки."""

    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: MiddlewareData,
    ) -> Any:
        async with self._session_factory() as session:  # type: AsyncSession
            data["db_session"] = session
            try:
                result = await handler(event, data)
            except Exception:
                await session.rollback()
                raise
            else:
                await session.commit()
                return result
