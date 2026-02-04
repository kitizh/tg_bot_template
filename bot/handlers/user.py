from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.common.handlers import BaseHandlers
from bot.services.user import UserService

import logging

log = logging.getLogger(__name__)

async def start(message: Message, user_service: UserService) -> None:
    log.info("User /start: %s", message.from_user.id if message.from_user else None)
    await message.answer(user_service.get_welcome_text())


class UserHandlers(BaseHandlers):
    """Хендлеры для базовых пользовательских команд."""

    def register(self) -> None:
        self.router.message.register(start, CommandStart())


router = UserHandlers().router
