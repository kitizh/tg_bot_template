from __future__ import annotations

from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisEventIsolation, RedisStorage
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from bot.core.config import Settings
from bot.infra.db import create_engine, create_session_factory
from bot.services.user import UserService

import logging

log = logging.getLogger(__name__)

@dataclass(slots=True)
class Container:
    """Контейнер ресурсов приложения (bot, dispatcher, redis, storage)."""
    settings: Settings
    bot: Bot
    dispatcher: Dispatcher
    redis: "redis.asyncio.Redis"
    storage: RedisStorage
    user_service: UserService
    db_engine: AsyncEngine | None
    db_session_factory: async_sessionmaker[AsyncSession] | None

    @classmethod
    async def create_polling(cls, settings: Settings) -> "Container":
        """Создать контейнер для режима polling."""
        import redis.asyncio as redis

        log.info("Initializing container resources")
        redis_client = redis.Redis.from_url(settings.redis_url)
        storage = RedisStorage(
            redis=redis_client,
            # сколько живет состояние пользователя в секундах
            state_ttl=60 * 60 * 24,
            # сколько живут данные в FSM
            data_ttl=60 * 60 * 24,
        )
        dispatcher = Dispatcher(
            storage=storage,
            # redis обеспечивает последовательную обработку обновлений от одного пользователя
            events_isolation=RedisEventIsolation(redis_client),
        )
        bot = Bot(token=settings.bot_token)
        user_service = UserService()
        db_engine = create_engine(settings) if settings.db_url else None
        db_session_factory = (
            create_session_factory(db_engine) if db_engine else None
        )
        log.info("Container initialized")
        return cls(
            settings=settings,
            bot=bot,
            dispatcher=dispatcher,
            redis=redis_client,
            storage=storage,
            user_service=user_service,
            db_engine=db_engine,
            db_session_factory=db_session_factory,
        )

    async def aclose(self) -> None:
        """Корректно закрыть все ресурсы контейнера."""
        log.info("Closing container resources")
        await self.bot.session.close()
        await self.redis.close()
        if self.db_engine is not None:
            await self.db_engine.dispose()
