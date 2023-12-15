import uuid
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from schemes import *


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
    await es_client.indices.create(
        index='movies',
        body=MOVIES_SCHEMA,
    )
    await es_client.indices.create(
        index='genres',
        body=GENRES_SCHEMA,
    )
    await es_client.indices.create(
        index='persons',
        body=PERSONS_SCHEMA,
    )


async def es_write_data(es_client):
    documents = []
    # es_create_scheme()
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

    await async_bulk(es_client, documents)
    await es_client.indices.refresh()


async def main():
    es_client = AsyncElasticsearch(hosts=['http://127.0.0.1:9200'])
    await es_create_scheme(es_client)
    await es_write_data(es_client)

    test_data = get_es_data()
    for item in test_data:
        index = item.pop('index')
        res = await es_client.search(index=index, body={'query': {'match_all': {}}})
        print(res)
        for hit in res['hits']['hits']:
            print(hit['_source'])

    await es_client.close()


import asyncio
asyncio.run(main())
