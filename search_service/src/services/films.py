import json
from functools import lru_cache

from fastapi import Depends

from models.films import FilmDetailResponseModel, FilmResponseModel, FilmSort
from services.utils.body_elastic import get_body_query, get_body_search
from services.base import BaseService
from services.base import get_base_service


class FilmService:
    """Сервис реализует возможности получения фильмов."""
    def __init__(self, base_service: BaseService):
        self.base_service = base_service

    async def get_by_id(
            self,
            film_id,
    ) -> FilmDetailResponseModel | None:
        """Метод возвращает фильм по id."""

        return await self.base_service.get_data_by_id(
            film_id,
            'movies',
            self.base_service.FILM_CACHE_EXPIRE_IN_SECONDS,
        )

    async def get_film_list(
            self,
            sort_by: FilmSort = FilmSort.down_imdb_rating,
            page_size: int = 50,
            page_number: int = 1,
            genre: str = None,
            actor: str = None,
            director: str = None,
            writer: str = None,
    ) -> list[FilmResponseModel | None]:
        """Метод возвращает список фильмов."""

        sort_order = 'desc' if sort_by == 'imdb_rating' else 'asc'
        body = get_body_search(
            size=page_size,
            sort_by='imdb_rating',
            offset=(page_size * page_number) - page_size,
            sort_order=sort_order,
            genre=genre,
            actor=actor,
            director=director,
            writer=writer
        )

        data_list = await self.base_service.get_list(
            index='movies',
            sort_by='imdb_rating',
            sort_order=sort_order,
            ttl=self.base_service.FILM_CACHE_EXPIRE_IN_SECONDS,
            body=body,
            page_size=page_size,
            page_number=page_number,
            genre=genre,
            actor=actor,
            director=director,
            writer=writer
        )

        return data_list

    async def search_film_by_query(
            self,
            query,
            page_size: int = 50,
            page_number: int = 1,
            process_id: str = None

    ) -> list[FilmResponseModel | None]:
        """Метод вовзращает список найденных фильмов."""

        body = get_body_query(
            field='title',
            value=query,
            size=page_size,
            offset=(page_size * page_number) - page_size,
        )

        data_list = await self.base_service.search_by_query(
            index='movies',
            body=body,
            query=query,
            ttl=self.base_service.FILM_CACHE_EXPIRE_IN_SECONDS,
            page_size=page_size,
            page_number=page_number,
            process_id=process_id
        )

        if process_id:
            await self.base_service.cache_handler.set_by_id(
                key=str(process_id),
                value=(
                    json.dumps([FilmResponseModel(**i).model_dump() for i in data_list])
                    if data_list
                    else json.dumps([])
                ),
                ttl=300,
            )
        return data_list


@lru_cache()
def get_film_service(
        base_service: BaseService = Depends(get_base_service)
) -> FilmService:
    return FilmService(base_service)
