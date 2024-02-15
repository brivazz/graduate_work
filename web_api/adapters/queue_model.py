
import uuid

from pydantic import BaseModel


class Message(BaseModel):
    """Модель сообщения брокера."""

    process_id: uuid.UUID
    file: str
