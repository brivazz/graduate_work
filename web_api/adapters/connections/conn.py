import aio_pika
from redis.asyncio import Redis
from loguru import logger

from adapters.broker.rabbit import rabbit_di
from adapters.cache.redis_cache import redis_di
from core.config import settings


async def on_startup() -> None:
    rabbit_di.rabbit = await aio_pika.connect_robust(
        settings.broker.get_amqp_uri()
    )
    logger.info('Rabbit connection success')
    logger.info(rabbit_di.rabbit)
    redis_di.redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
    )


async def on_shutdown() -> None:
    if rabbit_di.rabbit:
        await rabbit_di.rabbit.close()
    if redis_di.redis:
        await redis_di.redis.close()
