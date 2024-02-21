"""Модуль с классом базовой модели."""

from typing import Any

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Any) -> str:
    # orjson.dumps возвращает байты, соответствующие стандартному json.dumps, которые нам нужно декодировать
    # берется из https://docs.pydantic.dev/usage/exporting_models/#custom-json-deserialisation
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        model_load_json = orjson.loads
        model_dump_json = orjson_dumps
