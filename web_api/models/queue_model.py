from models.base import BaseOrjsonModel


class QueueMessage(BaseOrjsonModel):
    """Модель сообщения брокера."""

    file: str
