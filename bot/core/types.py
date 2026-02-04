from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from bot.core.container import Container
    from bot.services.user import UserService


class MiddlewareData(TypedDict, total=False):
    """Типизированный контейнер данных, доступных обработчикам через DI."""

    container: Container
    user_service: UserService
    db_session: AsyncSession
