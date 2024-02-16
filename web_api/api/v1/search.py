import uuid

from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from services.search_service import get_search_service, SearchService


router = APIRouter()


@router.post(
    '/search',
    description='Метод выполняет поиск по голосовому запросу',
)
async def search_data(
    file: UploadFile,
    service: SearchService = Depends(get_search_service),
) -> uuid.UUID:

    return await service.create_task(
        audio_file=file,
    )


@router.get(
    '/search/result',
    description='Метод возвращает результаты поиска из БД',
)
async def get_data(
    process_id: str,
    service: SearchService = Depends(get_search_service),
):
    # TODO: Необходимо возвращать модель
    result = await service.get_status_task(
        process_id=process_id,
    )
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Films not found')
    return result
