from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware

from bot.core.container import Container
from bot.core.types import MiddlewareData

class ContainerMiddleware(BaseMiddleware):
    """Прокидывает контейнер зависимостей в data обработчиков."""

    def __init__(self, container: Container) -> None:
        self._container = container

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: MiddlewareData,
    ) -> Any:
        data["container"] = self._container
        data["user_service"] = self._container.user_service
        return await handler(event, data)
