from aio_pika import connect_robust
from redis.asyncio import Redis

from broker.rabbit_broker import rabbit_di
from cache.redis_cache import redis_di
from core.config import settings


async def on_startup() -> None:
    rabbit_di.rabbit = await connect_robust(
        settings.get_amqp_uri()
    )
    redis_di.redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
    )


async def on_shutdown() -> None:
    if rabbit_di.rabbit:
        await rabbit_di.rabbit.close()
    if redis_di.redis:
        await redis_di.redis.close()
