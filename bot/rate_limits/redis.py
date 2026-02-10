from __future__ import annotations

from typing import Any


class RedisRateLimiter:
    """Redis-based rate limiter (fixed window)."""

    _SCRIPT = """
    local current = redis.call("INCR", KEYS[1])
    if tonumber(current) == 1 then
        redis.call("PEXPIRE", KEYS[1], ARGV[1])
    end
    if tonumber(current) > tonumber(ARGV[2]) then
        return 0
    end
    return 1
    """

    def __init__(self, redis: "redis.asyncio.Redis") -> None:
        self._redis = redis

    async def allow(self, key: str, *, limit: int, per: float) -> bool:
        per_ms = max(int(per * 1000), 1)
        result: Any = await self._redis.eval(self._SCRIPT, 1, key, per_ms, limit)
        return bool(result)
