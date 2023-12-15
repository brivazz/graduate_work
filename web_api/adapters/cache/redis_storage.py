from adapters import redis_di
from redis.asyncio import Redis
from core.config import settings


async def on_startup_redis() -> None:
    global redis
    redis_di.redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port
    )


async def on_shutdown_redis() -> None:
    if redis_di.redis:
        await redis_di.redis.close()
