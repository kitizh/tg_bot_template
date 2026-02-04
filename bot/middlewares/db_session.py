from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.types import MiddlewareData
import logging

log = logging.getLogger(__name__)

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
        log.debug("Opening DB session for update")
        async with self._session_factory() as session:  # type: AsyncSession
            data["db_session"] = session
            return await handler(event, data)
