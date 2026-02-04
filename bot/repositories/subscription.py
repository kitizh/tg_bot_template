from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from bot.models.subscription import Subscription
from bot.repositories.base import BaseRepository


class SubscriptionRepository(BaseRepository[Subscription]):
    """Репозиторий подписок."""

    model = Subscription

    async def get_by_user_id(self, user_id: int) -> Subscription | None:
        stmt = select(Subscription).where(Subscription.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def upsert_subscription(
        self,
        *,
        user_id: int,
        expires_at: datetime | None,
    ) -> Subscription:
        subscription = await self.get_by_user_id(user_id)
        if subscription is None:
            subscription = Subscription(user_id=user_id, expires_at=expires_at)
            await self.add(subscription)
        else:
            subscription.expires_at = expires_at
            await self._session.flush()
        return subscription

    async def set_expires_at(self, user_id: int, expires_at: datetime | None) -> None:
        subscription = await self.get_by_user_id(user_id)
        if subscription is None:
            subscription = Subscription(user_id=user_id, expires_at=expires_at)
            await self.add(subscription)
        else:
            subscription.expires_at = expires_at
            await self._session.flush()

    async def is_active(self, user_id: int, now: datetime | None = None) -> bool:
        subscription = await self.get_by_user_id(user_id)
        if subscription is None or subscription.expires_at is None:
            return False
        if now is None:
            now = datetime.now(subscription.expires_at.tzinfo)
        return subscription.expires_at > now

    async def extend_subscription(
        self,
        user_id: int,
        *,
        delta: timedelta,
    ) -> Subscription:
        subscription = await self.get_by_user_id(user_id)
        if subscription is None:
            subscription = Subscription(user_id=user_id, expires_at=None)
            await self.add(subscription)

        if subscription.expires_at is None:
            subscription.expires_at = datetime.now(timezone.utc) + delta
        else:
            subscription.expires_at = subscription.expires_at + delta
        await self._session.flush()
        return subscription
