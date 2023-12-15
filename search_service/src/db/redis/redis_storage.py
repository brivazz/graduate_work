from redis.asyncio import Redis


redis: Redis | None = None


async def on_startup_redis(host: str, port: str) -> None:
    global redis
    redis = Redis(host=host, port=port)


async def on_shutdown_redis() -> None:
    if redis:
        await redis.close()


async def get_redis():
    return redis