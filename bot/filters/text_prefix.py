from __future__ import annotations

from aiogram.filters import BaseFilter
from aiogram.types import Message


class TextPrefix(BaseFilter):
    """Проверяет, что текст сообщения начинается с префикса."""

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    async def __call__(self, message: Message) -> bool:
        return bool(message.text and message.text.startswith(self.prefix))
