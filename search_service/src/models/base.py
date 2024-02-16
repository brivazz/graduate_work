import orjson
from pydantic import BaseModel
from fastapi import Query


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        model_load_json = orjson.loads
        model_dump_json = orjson_dumps


class PaginateQueryParams:

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
        self.page_number = page_number
        self.page_size = page_size
