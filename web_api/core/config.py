from pathlib import Path

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent.parent.absolute()
from dotenv import load_dotenv
load_dotenv()

class BrokerSettings(BaseSettings):
    rabbit_host: str = Field("RABBIT_HOST", alias='rabbit_host')
    rabbit_port: str = Field("RABBIT_PORT")
    rabbit_user: str = Field("RABBIT_USER")
    rabbit_pass: str = Field("RABBIT_PASS")

    queue_name: str = Field("QUEUE_NAME")
    exchange_name: str = Field("EXCHANGE_NAME")

    def get_amqp_uri(self):
        return "amqp://{user}:{password}@{host}:{port}/".format(
            user=self.rabbit_user,
            password=self.rabbit_pass,
            host=self.rabbit_host,
            port=self.rabbit_port,
        )


class Settings(BaseSettings):
    project_name: str = Field(..., env="PROJECT_NAME")

    sentry_dsn: str = Field(..., env="SENTRY_DSN")

    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")

    broker: BrokerSettings = BrokerSettings()


settings = Settings()
