from uuid import UUID

from fastapi import APIRouter, Depends

from api.paginator import Paginator
from schemas.pastes import BasePasteSchema, PasteSchema, CreatePasteSchema
from services.pastes import PastesService, get_pastes_service


router = APIRouter(tags=['pastes'])


@router.get(
    '/pastes',
    response_model=list[BasePasteSchema],
    summary='Get pastes',
)
async def get_pastes(
    service: PastesService = Depends(get_pastes_service),
    paginator: Paginator = Depends(),
) -> list[BasePasteSchema]:
    pastes = await service.get_pastes(
        page_size=paginator.size,
        page_number=paginator.page,
    )
    return pastes


@router.post(
    '/pastes',
    response_model=PasteSchema,
    summary='Create new paste',
)
async def create_paste(
    paste: CreatePasteSchema,
    service: PastesService = Depends(get_pastes_service),
) -> PasteSchema:
    new_paste = await service.create_paste(
        title=paste.title,
        text=paste.text,
        expiration=paste.expiration,
        exposure=paste.exposure,
    )
    return new_paste


@router.get(
    '/pastes/{paste_pk}',
    response_model=PasteSchema,
    summary='Get paste by pk',
)
async def get_paste_by_pk(
    service: PastesService = Depends(get_pastes_service),
    paste_pk: str | UUID = None,
) -> PasteSchema:
    paste = await service.get_paste_by_pk(paste_pk)
    return paste
