import uuid
from aio_pika.exceptions import AMQPException
# from core.logger import logger
from functools import lru_cache
from redis.asyncio import Redis
from fastapi import Depends

import base64

# from graduate_work.web_api.adapters.broker.rabbit_broker.rabbit_manager import RabbitMq
# from adapters.broker.abstract import AbstractQueue
from adapters.cache.abstract import AbstractCache
from adapters.managers.redis_manager import RedisStorage
from core.config import settings

from adapters.broker.abstract import AbstractBrokerManager
from adapters.managers.broker_manager import get_broker_manager
from models.queue_model import QueueMessage
from fastapi import UploadFile
from loguru import logger
from adapters.cache.redis_cache.redis_di import get_redis


class SearchService:

    def __init__(
        self,
        storage_handler: AbstractCache,
        queue_handler: AbstractBrokerManager,
    ):
        self.storage_handler = storage_handler
        self.queue_handler: AbstractBrokerManager = queue_handler

    async def create_task(
        self,
        audio_file: UploadFile,
    ) -> uuid.UUID:
        """Метод получает на вход аудио файл и отдает uuid задачи."""

        process_id = uuid.uuid4()

        # print(await audio_file.read())

        file = base64.b64encode(await audio_file.read()).decode()
        try:
            if audio_file:
                print('Файл получен')

            await self.queue_handler.send_message(
                message=QueueMessage(file=file).model_dump_json().encode(),
                routing_key='events.files',
                correlation_id=process_id,
                priority=100,
            )
            print(process_id)
            return process_id

        except AMQPException as error:
            logger.error(f'Ошибка сервиса WebApi - {error}')

    async def get_status_task(
        self,
        process_id: str
    ):

        result = await self.storage_handler.get_by_id(
            key=process_id
        )
        # TODO: Поставить условие на проверку статуса if else
        print(result)
        return result


@lru_cache()
def get_search_service(
    storage: Redis = Depends(get_redis),
    broker_manager: AbstractBrokerManager = Depends(get_broker_manager)
) -> SearchService:
    return SearchService(
        storage_handler=RedisStorage(storage),
        queue_handler=broker_manager
    )
