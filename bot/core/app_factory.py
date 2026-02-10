from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from aiogram import Dispatcher, Router

from bot.core.config import Settings
from bot.core.container import Container
from bot.middlewares.container import ContainerMiddleware
from bot.middlewares.db_session import DbSessionMiddleware
from bot.middlewares.error_handler import ErrorHandlerMiddleware
from bot.middlewares.logging import LoggingMiddleware
from bot.middlewares.rate_limit import RateLimitMiddleware
from bot.middlewares.user_activity import UserActivityMiddleware

import logging

log = logging.getLogger(__name__)

@dataclass(slots=True)
class AppFactory:
    """Фабрика сборки приложения (container + dispatcher + routers)."""
    settings: Settings
    routers: Iterable[Router]

    async def create_container(self) -> Container:
        """Создать контейнер с ресурсами для polling режима."""
        return await Container.create_polling(self.settings)

    def create_dispatcher(self, container: Container) -> Dispatcher:
        """Подключить роутеры к dispatcher и вернуть его."""
        dispatcher = container.dispatcher
        self._setup_middlewares(dispatcher, container)
        for router in self.routers:
            dispatcher.include_router(router)
        log.info(
            "Rate limit config: msg=%s/%ss cmd=%s/%ss notify=%s",
            self.settings.rate_limit_limit,
            self.settings.rate_limit_period,
            self.settings.command_rate_limit_limit,
            self.settings.command_rate_limit_period,
            self.settings.rate_limit_notify,
        )
        log.info(
            "Dispatcher configured with routers and middleware. Routers: %s",
            [router.name for router in self.routers],
        )
        return dispatcher

    def _setup_middlewares(self, dispatcher: Dispatcher, container: Container) -> None:
        """Подключить базовые middleware приложения."""
        dispatcher.update.middleware(ErrorHandlerMiddleware())
        dispatcher.update.middleware(LoggingMiddleware())
        dispatcher.update.middleware(ContainerMiddleware(container))
        dispatcher.update.middleware(RateLimitMiddleware())
        if container.db_session_factory is not None:
            dispatcher.update.middleware(DbSessionMiddleware(container.db_session_factory))
            dispatcher.update.middleware(UserActivityMiddleware())
