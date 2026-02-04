from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable

from aiogram import Router

from bot.core.config import settings
from bot.core.app_factory import AppFactory

log = logging.getLogger(__name__)

@dataclass(slots=True)
class BotApp:
    """Главный класс приложения: собирает и запускает bot runtime."""

    routers: Iterable[Router] # Здесь хранятся все routers, которые были подключены в routers.py

    async def run_polling(self) -> None:
        """Запуск бота в режиме polling с корректным управлением ресурсами."""
        factory = AppFactory(settings=settings, routers=self.routers)
        container = await factory.create_container()
        try:
            factory.create_dispatcher(container)
            log.info("FSM storage: Redis")
            await container.dispatcher.start_polling(container.bot)
        finally:
            await container.aclose()
