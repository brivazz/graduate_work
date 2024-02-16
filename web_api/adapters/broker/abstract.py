"""Модуль с абстракным брокером сообщений."""

import abc
import uuid

from pydantic import BaseModel


class AbstractBrokerManager(abc.ABC):
    """Абстрактный брокер сообщений."""

    @abc.abstractmethod
    async def send_message(
        self,
        message: BaseModel,
        routing_key: str,
        correlation_id: uuid.UUID,
        priority: int | None = None,
    ):
        """Метод отправки сообщения в очередь."""
        raise NotImplementedError
