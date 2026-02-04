from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

TModel = TypeVar("TModel")


class BaseRepository(Generic[TModel]):
    """Базовый репозиторий с CRUD-операциями."""

    model: type[TModel]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, model_id: int) -> TModel | None:
        return await self._session.get(self.model, model_id)

    async def list(self, *, limit: int = 100, offset: int = 0) -> list[TModel]:
        stmt = select(self.model).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def add(self, instance: TModel) -> TModel:
        self._session.add(instance)
        await self._session.flush()
        return instance

    async def delete(self, instance: TModel) -> None:
        await self._session.delete(instance)
