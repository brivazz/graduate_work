import sys
import uuid
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk, BulkIndexError
from schemes import *
from core.config import settings


def get_es_data():
    movies = [{
        'index': 'movies',
        'id': str(uuid.uuid4()) if i != 0 else "1f90980e-e7c9-4fac-a1e4-f34409daeff2",
        'imdb_rating': 8.5,
        'genres': [
            {'id': '565', 'name': 'Sci-Fi'},
            {'id': '678', 'name': 'Action'}
        ],
        'title': 'The Star',
        'description': 'New World',
        'directors': [
            {'id': '123', 'name': 'Biba'},
            {'id': '112', 'name': 'Boba'},
        ],
        'actors_names': ['Stive Jobs', 'Bob Marley'],
        'writers_names': ['Kelvin Clein', 'Howard'],
        'actors': [
            {'id': '111', 'name': 'Stive Jobs'},
            {'id': '222', 'name': 'Bob Marley'}
        ],
        'writers': [
            {'id': '333', 'name': 'Kelvin Clein'},
            {'id': '444', 'name': 'Howard'}
        ],

    } for i in range(2)]

    genres = [
        {
            'index': 'genres',
            'id': '679',
            'name': 'Action',
            'description': 'Some test description!'
        },
        {
            'index': 'genres',
            'id': '566',
            'name': 'Sci-Fi',
            'description': 'Tsoy is alive!'
        }
    ]

    persons = [
        {
            'index': 'persons',
            'id': '222',
            'full_name': 'Bob Marley',
        },
        {
            'index': 'persons',
            'id': '111',
            'full_name': 'Stive Jobs',
        },
        {
            'index': 'persons',
            'id': '333',
            'full_name': 'Kelvin Clein'
        },
        {
            'index': 'persons',
            'id': '444',
            'full_name': 'Howard'
        },
        {
            'index': 'persons',
            'id': '123',
            'full_name': 'Biba'
        },
        {
            'index': 'persons',
            'id': '112',
            'full_name': 'Boba'
        }
    ]

    return movies + genres + persons


async def es_create_scheme(es_client):
    indexes = ['movies', 'genres', 'persons']
    for index in indexes:
        if await es_client.indices.exists(index=index):
            continue
        await es_client.indices.create(
            index=index,
            body=MOVIES_SCHEMA,
        )


async def es_write_data(es_client):
    documents = []
    test_data = get_es_data()
    for item in test_data:
        index = item.pop('index')
        documents.append(
            {
                "_index": index,
                "_id": item.get('id'),
                "_source": item,
            }
        )
    try:
        await async_bulk(es_client, documents)
        await es_client.indices.refresh()
    except BulkIndexError as e:
        pass


async def main(es_client):
    try:
        await es_create_scheme(es_client)
        await es_write_data(es_client)
    finally:
        await es_client.close()

if __name__ == '__main__':
    import asyncio
    async def run():
        es_client = AsyncElasticsearch(hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'])
        await main(es_client)

    asyncio.run(run())
