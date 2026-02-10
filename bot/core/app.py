from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable

from aiogram import Router
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

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
            await self._sync_commands(container.bot)
            log.info("FSM storage: Redis")
            await container.dispatcher.start_polling(container.bot)
        finally:
            await container.aclose()

    async def _sync_commands(self, bot: "Bot") -> None:
        """Синхронизировать команды с BotFather."""
        user_commands = [
            BotCommand(command="start", description="старт"),
            BotCommand(command="help", description="помощь"),
            BotCommand(command="reg", description="регистрация"),
            BotCommand(command="cancel", description="отменить регистрацию"),
            BotCommand(command="kb_inline", description="inline‑клавиатура"),
            BotCommand(command="kb_reply", description="reply‑клавиатура"),
            BotCommand(command="kb_hide", description="скрыть reply‑клавиатуру"),
        ]
        admin_commands = user_commands + [
            BotCommand(command="admin", description="админ‑панель"),
            BotCommand(command="stats", description="статистика"),
            BotCommand(command="broadcast", description="рассылка"),
        ]

        await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())
        for admin_id in settings.admin_ids:
            await bot.set_my_commands(
                admin_commands,
                scope=BotCommandScopeChat(chat_id=admin_id),
            )
