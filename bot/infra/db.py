from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from bot.core.config import Settings

import logging

log = logging.getLogger(__name__)


def create_engine(settings: Settings) -> AsyncEngine:
    """Создать async engine для SQLAlchemy."""
    if not settings.db_url:
        raise ValueError("DB_URL is required to create database engine")
    log.info("Creating async database engine")
    return create_async_engine(settings.db_url, pool_pre_ping=True)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Создать фабрику асинхронных сессий."""
    log.info("Creating async session factory")
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
