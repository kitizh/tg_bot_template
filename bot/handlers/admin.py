from __future__ import annotations

from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.common.handlers import BaseHandlers
from bot.filters.is_admin import IsAdmin
from bot.filters.rate_limit import RateLimit


class AdminHandlers(BaseHandlers):
    """Хендлеры админских команд (админы берутся из .env)."""

    def register(self) -> None:
        @self.router.message(Command("admin"), IsAdmin())
        async def admin_panel(message: Message) -> None:
            await message.answer(
                "Админ‑панель доступна ✅\n"
                "Команды: /stats, /broadcast"
            )

        @self.router.message(Command("stats"), IsAdmin())
        async def admin_stats(
            message: Message,
            db_session: AsyncSession | None = None,
        ) -> None:
            user_id = message.from_user.id if message.from_user else 0
            db_enabled = db_session is not None
            await message.answer(
                "Статистика (заготовка)\n"
                f"Ваш ID: {user_id}\n"
                f"DB: {'enabled' if db_enabled else 'disabled'}\n"
                "Подключите БД для расширенной статистики."
            )

        @self.router.message(
            Command("broadcast"),
            IsAdmin(),
            RateLimit(key_prefix="rate:cmd:broadcast", limit=1, per=30, notify=True),
        )
        async def admin_broadcast(message: Message) -> None:
            await message.answer(
                "Рассылка (заготовка).\n"
                "Добавим в следующем шаге: выбор аудитории, очередь и отчёт."
            )


router = AdminHandlers().router
