"""Модуль с DI для подключения к RabbitMQ."""

import aio_pika


rabbit: aio_pika.RobustConnection | None = None

async def get_rabbit() -> aio_pika.RobustConnection:
    """Функция зависимости для получения подключения к RabbitMQ."""
    return rabbit
