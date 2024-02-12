import base64
import json
import os
import sys
import re
import wave
from io import BytesIO

import requests
from celery import Celery
from vosk import KaldiRecognizer, Model, SetLogLevel
from googletrans import Translator
from loguru import logger
from aio_pika.abc import AbstractIncomingMessage

from core.config import settings

celery = Celery(
    __name__,
    broker_connection_retry=True,
    broker_connection_retry_on_startup=True,
)
celery.conf.broker_url = os.getenv(
    "CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.getenv(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379")


model = Model('./vosk-model-small-ru-0.22', lang='ru')
translator = Translator(service_urls=['translate.google.com'])

pattern_movie = re.compile(pattern=r"movie\s+([^?!.]+)")
pattern_person = re.compile(pattern=r"person\s+([^?!.]+)")
pattern_genre = re.compile(pattern=r"genre\s+([^?!.]+)")

METHODS = {
    "movie": "api/v1/films/search",
    "person": "api/v1/persons/persons/search",
}

SetLogLevel(0)

def recognize_audio(file):
    wf = wave.open(file, 'rb')
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    while True:
        data = wf.readframes(8000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)

    text = json.loads(rec.Result())["text"]
    translation = translator.translate(text, dest='en')
    return translation.text


@celery.task
def request_async_api(message: AbstractIncomingMessage):
    decode_body = json.loads(message.decode())
    process_id = decode_body.get("process_id")
    file = decode_body.get("file")
    file_in_memory = BytesIO(base64.b64decode(file.encode()))

    text = recognize_audio(file_in_memory)
    # if "movie" in text:
    #     name = pattern_movie.search(text)
    #     type_ = "movie"
    # elif "genre" in text:
    #     name = pattern_genre.search(text)
    #     type_ = "genre"
    # elif "person" in text:
    #     name = pattern_person.search(text)
    #     type_ = "person"
    # else:
    #     return
    logger.info(text)

    requests.get(
        # f"{settings.search_service_url}/{METHODS[type_]}",
        f"{settings.search_service_url}api/v1/films/search",
        # 'http://search_service:8001/api/v1/films/search',
        params=dict(query=text, process_id=process_id)
    )
