from adapters.broker.abstract import AbstractQueue
import orjson
from aio_pika import DeliveryMode, Exchange
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.channel import Channel
from aio_pika.connection import Connection
from aio_pika.message import Message
from loguru import logger
from typing import Any, Callable
import aio_pika


class RabbitMq(AbstractQueue):
    def __init__(self, rabbitmq_uri: str) -> None:
        self.rabbitmq_uri = rabbitmq_uri
        self.connection: Connection | None = None
        self.channel: Channel | None = None
        self.exchange: Exchange | None = None

    async def send(
        self,
        routing_key: str,
        data: dict,
        correlation_id,
    ) -> None:
        message = Message(
            body=self._serialize(data),
            content_type="application/json",
            correlation_id=correlation_id,
            delivery_mode=DeliveryMode.PERSISTENT
        )
        self.exchange = await self._exchange()
        await self.exchange.publish(message, routing_key, timeout=10)

    async def consume_queue(
            self,
            func: Callable,
            binding_keys: str | list[str],
            queue_name: str
    ):
        queue = await self.channel.declare_queue(queue_name, durable=True)

        if isinstance(binding_keys, list):
            for binding_key in binding_keys:
                await queue.bind(self.exchange, routing_key=binding_key)
        elif isinstance(binding_keys, str):
            await queue.bind(self.exchange, routing_key=binding_keys)

        async with queue.iterator() as iterator:
            message: AbstractIncomingMessage
            async for message in iterator:
                async with message.process(ignore_processed=True):
                    await func(message)

    @staticmethod
    def _serialize(data: Any) -> bytes:
        return orjson.dumps(data)

    async def close(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()

    async def send_data(self, *args, **kwargs):
        await self.send(
            routing_key=kwargs.get('routing_key'),
            data=kwargs.get('data'),
            correlation_id=kwargs.get('correlation_id')
        )
        logger.info(kwargs.get('routing_key'))

    async def read_data(self, *args, **kwargs):
        await self.consume_queue(
            func=kwargs.get('func'),
            binding_keys=kwargs.get('binding_keys'),
            queue_name=kwargs.get('queue_name'),
        )
