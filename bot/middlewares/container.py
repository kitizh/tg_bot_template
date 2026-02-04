from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware

from bot.core.container import Container
from bot.core.types import MiddlewareData

import logging

log = logging.getLogger(__name__)

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
        log.debug("Injecting container and services into handler context")
        data["container"] = self._container
        data["user_service"] = self._container.user_service
        return await handler(event, data)
