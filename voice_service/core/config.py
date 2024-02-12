from pathlib import Path

from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent.absolute()


class Settings(BaseSettings):
    # sentry_dsn: str = Field(..., env="SENTRY_DSN")

    rabbit_host: str = Field("RABBIT_HOST")
    rabbit_port: str = Field("RABBIT_PORT")
    rabbit_user: str = Field("RABBIT_USER")
    rabbit_pass: str = Field("RABBIT_PASS")

    search_service_url: str = Field('SEARCH_SERVICE_URL')

    celery_broker_url: str = Field(
        "redis://localhost:6379",
        env="CELERY_BROKER_URL"
    )
    celery_result_backend: str = Field(
        "redis://localhost:6379",
        env="CELERY_RESULT_BACKEND"
    )

    def get_amqp_uri(self):
        return "amqp://{user}:{password}@{host}:{port}/".format(
            user=self.rabbit_user,
            password=self.rabbit_pass,
            host=self.rabbit_host,
            port=self.rabbit_port
        )


settings = Settings()
