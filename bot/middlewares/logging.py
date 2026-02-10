from __future__ import annotations

import logging
import time
from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Update

log = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """Логирует входящие апдейты и время обработки."""

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        started = time.monotonic()
        kind, user_id, chat_id, payload = _describe_update(event)
        log.info("Update received: type=%s user_id=%s chat_id=%s payload=%s", kind, user_id, chat_id, payload)
        try:
            return await handler(event, data)
        finally:
            duration_ms = int((time.monotonic() - started) * 1000)
            log.info("Update handled: type=%s user_id=%s duration_ms=%s", kind, user_id, duration_ms)


def _describe_update(event: Update) -> tuple[str, int | None, int | None, str | None]:
    message = event.message or event.edited_message
    if message:
        user_id = message.from_user.id if message.from_user else None
        chat_id = message.chat.id if message.chat else None
        text = (message.text or message.caption or "").strip()
        payload = text[:120] if text else None
        return ("message", user_id, chat_id, payload)

    callback = event.callback_query
    if callback:
        user_id = callback.from_user.id if callback.from_user else None
        chat_id = callback.message.chat.id if callback.message and callback.message.chat else None
        payload = (callback.data or "").strip()[:120] if callback.data else None
        return ("callback_query", user_id, chat_id, payload)

    return ("update", None, None, None)
