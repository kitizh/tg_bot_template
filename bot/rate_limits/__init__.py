from bot.rate_limits.redis import RedisRateLimiter

default_limiter: RedisRateLimiter | None = None


def init_default_limiter(redis: "redis.asyncio.Redis") -> None:
    global default_limiter
    default_limiter = RedisRateLimiter(redis)

__all__ = ["RedisRateLimiter", "default_limiter", "init_default_limiter"]
