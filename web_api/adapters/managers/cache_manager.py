import orjson
from redis.asyncio import Redis

from adapters.cache.abstract import AbstractCache


class RedisStorage(AbstractCache):
    def __init__(
            self,
            redis: Redis,
    ):
        self.redis = redis

    async def get_by_id(self, *args, **kwargs) -> dict | None:
        data = await self.redis.get(kwargs.get('key'))
        return orjson.loads(data) if data else None

    async def set_by_id(self, *args, **kwargs) -> None:
        await self.redis.set(
            kwargs.get('key'),
            kwargs.get('value'),
            kwargs.get('ttl'),
        )
