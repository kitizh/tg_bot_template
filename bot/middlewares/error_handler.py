from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Update

class ErrorHandlerMiddleware(BaseMiddleware):
    """Перехватывает исключения и отправляет пользователю вежливое сообщение."""

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except asyncio.CancelledError:
            raise
        except Exception:
            await _notify_user(event)
            return None


async def _notify_user(event: Update) -> None:
    message = event.message or event.edited_message
    if message is not None:
        await message.answer("Произошла ошибка. Попробуйте позже.")
        return

    callback = event.callback_query
    if callback is not None:
        await callback.answer("Произошла ошибка. Попробуйте позже.", show_alert=True)
