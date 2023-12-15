from elasticsearch import AsyncElasticsearch


elastic: AsyncElasticsearch | None = None


async def on_startup_es(hosts: list) -> None:
    global elastic
    elastic = AsyncElasticsearch(hosts=hosts)


async def on_shutdown_elastic() -> None:
    if elastic:
        await elastic.close()

async def get_elastic():
    return elastic
