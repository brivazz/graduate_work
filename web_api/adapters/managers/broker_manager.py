import uuid

from fastapi import Depends

from adapters.broker.abstract import AbstractBrokerManager
from adapters.broker.rabbit.rabbit_broker import RabbitMQMessageSender, get_broker


class BrokerManager(AbstractBrokerManager):
    """Класс реализации брокера сообщений."""

    def __init__(self, sender: RabbitMQMessageSender) -> None:
        self.sender = sender

    async def send_message(
        self,
        message: dict,
        routing_key: str,
        correlation_id: uuid.UUID,
        priority: int | None = None,
    ):
        await self.sender.send(
            message=message,
            routing_key=routing_key,
            correlation_id=correlation_id,
            priority=priority,
        )


async def get_broker_manager(sender: AbstractBrokerManager = Depends(get_broker)):
    return BrokerManager(sender)
