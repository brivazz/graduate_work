from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core.config import settings
from db.redis.redis_storage import on_startup_redis, on_shutdown_redis
from db.elastic.elastic_storage import on_startup_es, on_shutdown_elastic


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup_redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    )
    await on_startup_es(
        hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}']
    )
    yield
    await on_shutdown_redis()
    await on_shutdown_elastic()


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8001, reload=True)
