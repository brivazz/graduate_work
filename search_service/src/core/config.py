from logging import config as logging_config
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from loguru import logger

from core.logger import LOGGING

load_dotenv()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    PROJECT_NAME: str = Field('PROJECT_NAME')

    REDIS_HOST: str = Field('REDIS_HOST')
    REDIS_PORT: int = Field('REDIS_PORT')

    ELASTIC_HOST: str = Field('ELASTIC_HOST')
    ELASTIC_PORT: int = Field('ELASTIC_PORT')


settings = Settings()
