from __future__ import annotations

from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.common.handlers import BaseHandlers
from bot.filters.is_admin import IsAdmin

import logging

log = logging.getLogger(__name__)


class AdminHandlers(BaseHandlers):
    """Хендлеры админских команд (админы берутся из .env)."""

    def register(self) -> None:
        @self.router.message(Command("admin"), IsAdmin())
        async def admin_panel(message: Message) -> None:
            log.info("Admin /admin: %s", message.from_user.id if message.from_user else None)
            await message.answer(
                "Админ‑панель доступна ✅\n"
                "Команды: /stats, /broadcast"
            )

        @self.router.message(Command("stats"), IsAdmin())
        async def admin_stats(
            message: Message,
            db_session: AsyncSession | None = None,
        ) -> None:
            log.info("Admin /stats: %s", message.from_user.id if message.from_user else None)
            user_id = message.from_user.id if message.from_user else 0
            db_enabled = db_session is not None
            await message.answer(
                "Статистика (заготовка)\n"
                f"Ваш ID: {user_id}\n"
                f"DB: {'enabled' if db_enabled else 'disabled'}\n"
                "Подключите БД для расширенной статистики."
            )

        @self.router.message(Command("broadcast"), IsAdmin())
        async def admin_broadcast(message: Message) -> None:
            log.info("Admin /broadcast: %s", message.from_user.id if message.from_user else None)
            await message.answer(
                "Рассылка (заготовка).\n"
                "Добавим в следующем шаге: выбор аудитории, очередь и отчёт."
            )


router = AdminHandlers().router
