from __future__ import annotations

from aiogram.types import Message

from bot.common.handlers import BaseHandlers


class FallbackHandlers(BaseHandlers):
    """Хендлер по умолчанию для сообщений без совпавших фильтров."""

    def register(self) -> None:
        @self.router.message()
        async def echo_fallback(message: Message) -> None:
            await message.copy_to(chat_id=message.chat.id)


router = FallbackHandlers().router
