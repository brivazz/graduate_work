import json
from redis.asyncio import Redis

from adapters.cache.abstract import AbstractStorage


class RedisStorage(AbstractStorage):
    def __init__(
            self,
            redis: Redis,
    ):
        self.redis = redis

    async def get_by_id(self, *args, **kwargs) -> dict | None:
        data = await self.redis.get(kwargs.get('key'))
        return json.loads(data) if data else None

    async def set_by_id(self, *args, **kwargs) -> None:
        await self.redis.set(
            kwargs.get('key'),
            kwargs.get('value'),
            kwargs.get('ttl'),
        )
