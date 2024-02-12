"Модуль для создания подключения к RabbitMQ."

from typing import Optional

import aio_pika
from fastapi import Depends
from pydantic import BaseModel

from adapters.broker.rabbit.rabbit_di import get_rabbit


class RabbitMQ:
    """Класс для создания подключения к RabbitMQ."""

    def __init__(self, connection: aio_pika.RobustConnection) -> None:
        """Инициализация объекта."""
        self.connection = connection
        self.channel: Optional[aio_pika.RobustChannel] = None
        self.exchange: Optional[aio_pika.Exchange] = None

    async def init_required(self):
        """Асинхронная инициализация обменника в брокере."""
        self.channel = await self.connection.channel()
        # self.exchange = await self.channel.get_exchange('topic_v1')
        self.exchange = await self.channel.declare_exchange('topic_v1', auto_delete=True)

    # async def _declare_queue(self) -> None:
    #     """Создание очередей."""
    #     await self.channel.declare_queue('queue_name', durable=True)

    async def publish(self, msg: BaseModel, routing_key: str, priority: int | None = None):
        """Публикация сообщения в брокере."""
        await self.exchange.publish(
            aio_pika.Message(body=msg.json().encode(), priority=priority),
            routing_key=routing_key
        )
        print(f'Message {msg} отправлено', f' в очередь {routing_key}')


from loguru import logger
# async def get_broker(connection: aio_pika.RobustConnection = Depends(get_rabbit)):
async def get_broker():
    connection = await get_rabbit()
    logger.info(connection)
    broker = RabbitMQ(connection)
    await broker.init_required()
    return broker