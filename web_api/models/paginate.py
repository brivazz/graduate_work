"""Модуль с классом пагинации."""

from fastapi import Query


class PaginateQueryParams:
    """Класс пагинации."""

    def __init__(
            self,
            page_number: int = Query(
                1,
                title='Page number.',
                description="Page number to return.",
                ge=1,
            ),
            page_size: int = Query(
                50,
                title="Size of page.",
                description="The number of records returned per page",
                ge=1,
                le=500,
            ),
    ):
        """Инициализатор класса."""
        self.page_number = page_number
        self.page_size = page_size
