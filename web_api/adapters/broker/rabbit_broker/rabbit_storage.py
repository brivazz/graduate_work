"Модуль для создания подключения к RabbitMQ."

from typing import Optional

import aio_pika
from aio_pika import Exchange
from aio_pika.channel import Channel
from aio_pika.connection import Connection


class RabbitMQ:
    """Класс для создания подключения к RabbitMQ."""

    def __init__(self, rabbitmq_uri: str) -> None:
        """Инициализация обекта."""
        self.uri: str = rabbitmq_uri
        self.connection: Optional[Connection] = None
        self.channel: Optional[Channel] = None
        self.exchange: Optional[Exchange] = None

    async def _connect(self, topic_name: str = 'topic_v1') -> Connection:
        """Создает соединение по протоколу AMQP."""
        if self.connection is None:
            self.connection = await aio_pika.connect_robust(self.uri)
        return self.connection

    async def _create_channel(self) -> Channel:
        """В рамках соединения создает канал."""
        if self.channel is None:
            connection = await self._connect()
            self.channel = await connection.channel()
        return self.channel

    async def _exchange(self) -> Exchange:
        """Точка входа ("Обменник") для публикации всех сообщений."""
        if self.exchange is None:
            self.channel = await self._create_channel()
            self.exchange = await self.channel.get_exchange('topic_v1')
        return self.exchange
