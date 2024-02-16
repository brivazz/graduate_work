"""Модуль с реализацией абстрактного брокера сообщений."""

import uuid
import aio_pika
from fastapi import Depends

from adapters.broker.rabbit.rabbit_di import get_rabbit
from core.config import settings


class RabbitMQMessageSender:
    """Класс для создания подключения к RabbitMQ."""

    def __init__(self, connection: aio_pika.RobustConnection) -> None:
        """Инициализация объекта."""
        self.connection = connection
        self.channel: aio_pika.RobustChannel | None = None
        self.exchange: aio_pika.Exchange | None = None

    async def create_queue_and_bind(self) -> None:
        """Асинхронная инициализация обменника в брокере."""
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            name=settings.broker.exchange_name,
            type=aio_pika.ExchangeType.TOPIC,
        )
        queue = await self.channel.declare_queue(settings.broker.queue_name, durable=True)
        await queue.bind(self.exchange, 'events.files')

    async def send(
        self,
        message: bytes,
        routing_key: str,
        correlation_id: uuid.UUID,
        priority: int | None = None,
    ) -> None:
        """Публикация сообщения в брокере."""
        await self.exchange.publish(
            aio_pika.Message(
                body=message,
                content_type="application/json",
                priority=priority,
                correlation_id=correlation_id,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
            routing_key=routing_key,
        )


async def get_broker(connection: aio_pika.RobustConnection = Depends(get_rabbit)) -> RabbitMQMessageSender:
    """DI брокера сообщений."""
    broker = RabbitMQMessageSender(connection)
    await broker.create_queue_and_bind()
    return broker
